from flask import Blueprint, Flask, request, jsonify, render_template, session

import geopandas as gpd
import plotly.express as px
import plotly.io as pio

import joblib
import pandas as pd
import requests
import time
import re
import json
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
merged_df = joblib.load(os.path.join(BASE_DIR, "data", "merged_df.joblib"))
food = pd.read_csv(os.path.join(BASE_DIR, "data", "wfp_food_prices_cod.csv"))

food_categories = ['meat, fish and eggs','cereals and tubers', 'pulses and nuts']
commodities = ['goat', 'chicken', 'beef','cassava', 'beans']
outbreak_list = ['2008-12-1', '2012-06-01', '2014-08-01', '2018-05-01',
                  '2020-05-01', '2021-05-01', '2021-10-01', '2025-08-01', '2026-05-01']

food_cat_dict = {'goat':'meat, fish and eggs', 'chicken':'meat, fish and eggs', 'beef':'meat, fish and eggs',
                 'cassava':'cereals and tubers', 
                 'beans':'pulses and nuts'}

## BLUEPRINT INSTANCE
ebola = Blueprint(
    "ebola_portal",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/ebola_portal/static",  # avoids clashing with other blueprints' /static
)


# APP ROUTE
@ebola.route("/", methods=["GET", "POST"]) 
def results():
    map_variable = session.get("map_variable", "cases_per_million")
    food_commodity = session.get("food_commodity", "goat")
    
    if request.method == 'POST':
        submitted_form = request.form.get("form_id")
        if submitted_form == "ebola_form":
            map_variable = request.form.get("highlight")
            session["map_variable"] = map_variable
        elif submitted_form == "food_form":
            food_commodity = request.form.get("plot_var")
            session["food_commodity"] = food_commodity

    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print("map_variable:", repr(map_variable))

    food_category = food_cat_dict[food_commodity]

    ## FILTER FOOD DATAFRAME
    food_cat = food[food['category']==food_category]
    food_prices = food_cat[food_cat["commodity"].str.contains(food_commodity, case=False, na=False)]

    ## WRANGLE DATA/TIME POINTS
    food_prices["date"] = pd.to_datetime(food_prices["date"], dayfirst=True)  # format looks like DD/MM/YYYY
    food_prices["month"] = food_prices["date"].dt.to_period("M")

    ## PRODUCE MONTHLY DATAPOINTS
    monthly_avg = food_prices.groupby("month")["usdprice"].mean().reset_index()
    monthly_avg["month"] = monthly_avg["month"].dt.to_timestamp()

    ## PRODUCE FOOD FIGURE
    food_fig = px.line(monthly_avg, x="month", y="usdprice", markers=True,
                title=f"Monthly average price of {food_commodity}")
    food_fig.update_layout(xaxis_title="Month", yaxis_title="Average price (USD)")

    ## ADD EBOLA OUTBREAKS
    for date in outbreak_list:
        food_fig.add_vline(
            x=pd.Timestamp(date),
            line_width=1,
            line_dash="dash",
            line_color="red",
        )

    ## PRODUCE EBOLA FIGURE
    geojson_dict = json.loads(merged_df.to_json())
    ebola_fig = px.choropleth_mapbox(
        merged_df,
        geojson=geojson_dict,
        locations="adm1_pcode",
        featureidkey="properties.adm1_pcode",
        color=map_variable,
        hover_data=["adm1_name", "cases_per_million", "deaths_per_million", map_variable],
        color_continuous_scale="OrRd",
        mapbox_style="open-street-map",
        center={"lat": -2.5, "lon": 23.5},
        zoom=3.9,
        opacity=0.7,
    )
    ebola_fig = ebola_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    ebola_html = pio.to_html(ebola_fig, full_html=False, include_plotlyjs="cdn")
    food_html = pio.to_html(food_fig, full_html=False)

    return render_template("results_page.html", ebola_fig=ebola_html, food_fig=food_html)

