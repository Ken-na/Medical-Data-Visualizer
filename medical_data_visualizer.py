import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")
# Add 'overweight' column
    #To determine if a person is overweight, first calculate their BMI by dividing their weight in kilograms by the square of their height in meters.
df['overweight'] = np.where(df['weight']/((df['height']/100)**2) > 25, 1, 0)

#print(df)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = np.where(df['cholesterol'] < 2, 0, 1)
df['gluc'] = np.where(df['gluc'] < 2, 0, 1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars =['cardio'], value_vars =['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'], var_name ='variable', value_name ='value')

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index = False).size().rename(columns={'size':'total'})

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(data=df_cat, x='variable', hue='value', col='cardio', y='total', kind='bar')

    # Do not modify the next two lines
        #had to add.fig to return correct answer
    fig.savefig('catplot.png')
    return fig.fig

# Draw Heat Map
def draw_heat_map():
    #data has no null values.
    #print(df.isnull().sum())

    # Clean the data
    df_heat = df.where((df['ap_lo'] <= df['ap_hi']) &
                    (df['height'] >= df['height'].quantile(0.025)) &
                    (df['height'] <= df['height'].quantile(0.975)) &
                    (df['weight'] >= df['weight'].quantile(0.025)) &
                    (df['weight'] <= df['weight'].quantile(0.975))).dropna()

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12,12)) #was 9,9

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, mask=mask, square=True, annot=True, linewidths=.5, fmt=".1f")#, center=0)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
