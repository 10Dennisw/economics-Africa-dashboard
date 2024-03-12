# Quick Introduction 
This dashboard visualises economic data from countries. More precisely, the visualisation maps specific wealth through measuring Gross Domestic Product (GDP). GDP is calculating through adding the consumption, investment, net government expenditure and net exports. The dashboard is designed for economists with a background knowledge in the data.

The data is from Kaggle and gathered from the world bank. The data is panel data; therefore, contains the numerous data on different countries over a period. 

The dashboard was created using the Dash and Plotly library.  

The dashboard contains different pages which shows the different aspects of the data.
- Page 1 shows a general overview of the GDP and population in each country, distribution of the total GDP in Africa and Bar Chart. Page 1 contains a slider meaning that the user can view the information over a period.
- Page 2 shows the growth of wealth in Africa, by showing the data in the first and final year. 
- Page 3 shows the specific GDP per capita. This highlights the wealth per individual.


# User Guide

**Introduction**

Welcome to the "Evolution of African GDP: Overview" page of the dashboard. This interactive page provides visual insights into the GDP and population trends across African countries over selected years.

## Page 1: An Overview of the Evolution of African GDP

Upon loading page 1, you will see several components:
1. **Year Slider**: A slider at the top allows you to select the year for which you want to view data. Slide across to change the year and update all visualizations correspondingly.
2. **Map Charts**:
    - **Choropleth Map of GDP**: Shows the GDP distribution across African countries, with varying shades of red indicating different GDP levels.
    - **Map of GDP with Population Bubbles**: Overlays population data on the GDP map, with bubble sizes representing the population of each country.
3. **Bar Chart**: Displays the top five African economies in terms of GDP for the selected year.
4. **Pie Chart**: Shows the distribution of GDP among the top five economies and others, providing a percentage breakdown of their contribution to the total GDP.

**Using the Dashboard**

- **Selecting a Year**: Use the year slider to select the desired year. All visualizations will automatically update to reflect the data of the selected year.
- **Interacting with Charts**:
    - Hover over any element in the maps, bar chart, or pie chart to see detailed information like country name, GDP, and population.
    - Use the legends to highlight data in the pie and bar charts.
      
**Interpretation Tips**

- **Map Visualization**: Look for color intensity changes over years in the choropleth map to gauge GDP growth. Larger bubbles in the population map indicate more populous nations.
- **Bar Chart**: Compare the heights of bars to understand the relative size of economies. Notice how rankings and sizes change over years.
- **Pie Chart**: Check the pie sections to see how dominant the top economies are in terms of GDP contribution.
  
**Page 1: Conclusion**

This dashboard page is designed to provide a comprehensive overview of the African GDP landscape, allowing for interactive exploration and a deeper understanding of economic trends across the continent. Use the interactive elements to engage with the data and uncover insights into the economic dynamics of African countries.

## Page 2: Africa's Top 5 Economies - Comparison between 2000 to 2022

1. **Pie Charts Comparison**
    - The page opens with two pie charts side-by-side showing the GDP distribution in 2000 and 2022.
    - Hover over the segments to view detailed GDP figures for each economy.
    - The color scheme remains consistent for each country across charts to aid in visual comparison.
2. **Scatter Plot: GDP Trend Analysis**
    - Below the pie charts, a scatter plot illustrates the year-wise GDP trend from 2000 to 2022 for the top economies.
    - Each line represents a different country, color-coded to match the pie chart for continuity.
    - Hover over points to see exact GDP figures per year for each country.
3. **Bar Chart: GDP Growth Comparison**
    - Next to the scatter plot, a bar chart compares the GDP of these economies in 2000 and 2022 side-by-side.
    - This visual helps to quickly assess how each economy has progressed over the 22-year period.
    - Hover to get the exact GDP values and compare the growth rate visually.
   
**Using the Dashboard**

- **Educational Tool**: This page serves as an educational tool for understanding the complexities and growth patterns of African economies.
- **Data-Driven Decisions**: By offering a historical perspective, it assists researchers, students, and policymakers in making informed decisions based on economic trends.

**Interpreting  the Dashboard**
  
- **Understanding Economic Growth**: Use the pie charts to see the proportional changes and the bar chart for the absolute growth in GDP.
- **Yearly Trend Insights**: The scatter plot provides a detailed look at the annual economic performance and growth trajectory of each country.
- **Comparative Analysis**: By comparing the 2000 and 2022 data points, users can understand significant shifts in the economic landscape of Africa.
- **Dynamic Data Exploration**: All charts offer interactive tooltips, providing more context and specific data as you hover over different elements.
- **Visual Consistency**: The use of color and design ensures a coherent and unified visual experience, aiding in the comparison and analysis of data.

**Page 2: Conclusion**

Page 2 of the dashboard offers an immersive experience to explore and understand the economic changes in Africa’s top 5 economies over two decades. By interacting with the data through well-designed visualizations, users gain deeper insights into the economic progress and transformations in the continent.

## Page 3: Africa: GDP per Capita

Upon loading page 3, you will see several components: 

1. **Year Selection Slider**
    - At the top of the page, a slider allows you to select the year of interest.
    - **Usage**: Drag the slider to change the year. The visualizations on the page will automatically update to reflect data from the selected year.
2. **GDP per Capita Map**
    - A choropleth map displays the logarithmic value of GDP per capita for each African country.
    - **Usage**: Hover over countries on the map to see detailed GDP per capita data for the selected year. Small island nations like Seychelles and Mauritius are highlighted with detailed insets for clarity.
3. **GDP per Capita Histogram**
    - This histogram shows the distribution of GDP per capita across African countries.
    - **Usage**: Analyse the spread and concentration of GDP per capita values, which helps in understanding the economic diversity and disparity within the continent.
4. **Top 10 Economies Bar Chart**
    - A bar chart illustrates the top 10 African countries with the highest GDP per capita for the selected year.
    - **Usage**: Identify the leading economies in terms of GDP per capita and understand their relative economic positions.
   
**Using the Dashboard**

- Utilize the year slider to track economic changes over time and identify trends or shifts in the economic landscape of Africa.
- Hover over visual elements in the charts and maps to extract specific data points and detailed insights.
- Use the comparative view provided by the bar chart and histogram to understand the broader economic context of the continent's top economies.

**Interpretation Tips**

- The **map** provides a geographical representation of wealth distribution, allowing for regional economic analysis.
- The **histogram** offers insight into the economic equality or inequality among the African nations, showing how GDP per capita is distributed.
- The **bar chart** not only shows the top performers but also places the average GDP per capita in context, illustrating the economic gap within the continent.

**Page 3: Conclusion**

Page 3 of the dashboard offers an immersive and detailed examination of the GDP per capita across African countries, providing users with powerful tools for economic analysis and insight generation. By interacting with the visualizations, users can uncover nuanced understandings of the economic health and disparities across the continent. 

