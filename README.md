# ebola-portal

This portal displays the number of cases and deaths per million inhabitants per state, and then provides the option to compare these to the number of displacements through conflict (per million), the deforestation rate, and the number of attacks on healthcare workers per state. I hypothesise that the displacement of nature through deforestation and human migration as well as the damage of healthcare resources may be triggers for outbreaks. 
A second figure displays the cost of selected staple foods over time, with the beginnings of outbreaks highlighted as red lines on the curve. I wanted to investigate whether the cost of food, particularly protein, may force individuals to defer to bushmeat and trigger an outbreak.

## Getting Started
To run on your localhost please download the directory 'website_blueprint'. Alternately, you can clone the project and run it locally.

## Run Locally

Clone the project

```bash
  git clone https://github.com/fraseralex96/ebola-portal-built-into-personal-website-
```

Go to the project directory

```bash
  cd ebola-portal-built-into-personal-website-/website_blueprint
```

Install dependencies

```bash
  pip install flask==2.2.2
  pip install rpy2==3.5.1
  pip install pandas==1.5.3
  pip install seaborn==0.12.2
  pip install matplotlib==3.7.0
  pip install requests==2.21.0
  pip install flask_sqlalchemy==3.0.2
  pip install SQLAlchemy==1.4.46
  pip install ld_plot==0.0.2.1
  pip install numpy==1.24.2

```

Running the website

In your commandline in the 'website_blueprint' directory run the following command:

```bash
  python main_app.py
```
Copy the localhost URL and paste it into your browser (for best user experience please use Google Chrome or Safari).

