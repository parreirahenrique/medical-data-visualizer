import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add "overweight" column
df["overweight"] = df["weight"] / ((df["height"] / 100) ** 2)

# # Normalize data by making 0 always good and 1 always bad. If the value of "cholesterol" or "gluc" is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[(df["cholesterol"] == 1), "cholesterol"] = 0
df.loc[(df["cholesterol"] > 1),  "cholesterol"] = 1

df.loc[(df["gluc"] == 1), "gluc"] = 0
df.loc[(df["gluc"] > 1),  "gluc"] = 1

df.loc[(df["overweight"] <= 25), "overweight"] = 0
df.loc[(df["overweight"] > 25),  "overweight"] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from "cholesterol", "gluc", "smoke", "alco", "active", and "overweight".
    df_cat = pd.melt(df, id_vars="cardio", value_vars=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"])
    
    # Group and reformat the data to split it by "cardio". Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    # df_cat
    
    # Draw the catplot with "sns.catplot()"
    
    # Get the figure for the output
    fig, (axis1, axis2) =  plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
    sns.countplot(ax=axis1, x="variable", hue="value", data=df_cat.loc[(df_cat["cardio"] == 0)])
    axis1.set_title("cardio = 0")
    axis1.set_xlabel("variable")
    axis1.set_ylabel("total")
    axis1.get_legend().remove()
    axis1.spines['top'].set_visible(False)
    axis1.spines['right'].set_visible(False)
    sns.countplot(ax=axis2, x="variable", hue="value", data=df_cat.loc[(df_cat["cardio"] == 1)])
    axis2.set_title("cardio = 1")
    axis2.set_xlabel("variable")
    axis2.set_ylabel("")
    # axis2.set_yticks()
    axis2.tick_params(top=False,
               bottom=True,
               left=True,
               right=False,
               labelleft=False,
               labelbottom=True)
    axis2.legend([0, 1], title="value", loc=(1, 0.5), frameon=False)
    axis2.spines['top'].set_visible(False)
    axis2.spines['right'].set_visible(False)

    # Do not modify the next two lines
    fig.savefig("catplot.png")
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df["ap_lo"] <= df["ap_hi"]) & (df["height"] >= df["height"].quantile(0.025)) & (df["height"] <= df["height"].quantile(0.975)) & (df["weight"] >= df["weight"].quantile(0.025)) & (df["weight"] <= df["weight"].quantile(0.975))]
    
    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=bool).T
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(14,6))
    
    # Draw the heatmap with "sns.heatmap()"
    sns.heatmap(ax=ax, data=corr, annot=True, fmt=".1f" ,mask=mask)

    # Do not modify the next two lines
    fig.savefig("heatmap.png")
    return fig
