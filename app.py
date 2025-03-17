from utilities.tools import get_indicators, get_countries, get_groups, get_regions, get_data
import streamlit as st
import pandas as pd


def main():
    """
    Main function for the app. Sets up the Streamlit app's title and sidebar, and 
    handles the user's selection of indicators, groupby (country, group, region), 
    and the specific items in the selected groupby. When the user clicks "Get Data", 
    prints the selected indicators and countries.
    """
    data = None
    if 'selected' not in st.session_state:
        st.session_state.selected = None 

    st.set_page_config(page_title="IMF Data Mapper", page_icon="🌍", layout="wide")

    with st.sidebar:
        st.title("IMF Data Mapper")
        st.write("## Select Data")
        indicators_data = get_indicators()
        # indicators = indicators_data['indicator_name']
        indicator = st.multiselect("Select Indicators",get_indicators()['indicator_name'], default='Real GDP growth')
        # groupby = st.radio("I want data by:",['Country', 'Region'],
        #                 captions=['Ex:***India, USA...***','Ex: ***East Asia, Europe...***'])
        country = st.multiselect('Select Country',get_countries()['country_name'], default='India')
        # if groupby == 'Country':
        #     country = st.multiselect('Select Country',get_countries()['country_name'], default='India')
        # else:
        #     country = None

        # if groupby == 'Group':
        #     group = st.multiselect('Select Group',get_groups()['group_name'], default='Oil-exporting countries')
        # else:
        #     group = None

        # if groupby == 'Region':
        #     region = st.multiselect('Select Region',get_regions()['region_name'], default='Europe')
        # else:
        #     region = None

        # if st.button("Get Data"):
        #     with st.spinner():
        data = get_data(indicator, country) #add region and group later when you correct it
        st.success("Data fetched successfully!")
    if data is not None:
        st.write("## Data")
        tab1,tab2 = st.tabs(["Download Raw Data","Data Visualizations"])
        with tab1:
            try:
                csv = data.to_csv(index=False, encoding = 'utf-8')
                meta_data = {'Rows': data.shape[0], 'Columns': data.shape[1], 'Column Names': list(data.columns)}
                mtcol1,mtcol2,mtcol3 = st.columns([1,1,8])
                mtcol1.metric("Rows",meta_data['Rows'])
                mtcol2.metric("Columns",meta_data['Columns'])
                mtcol3.metric("Column Names",', '.join(meta_data['Column Names']))

                col1,col2 = st.columns([.75,.25])
                
                with col1:
                    st.write("#### Download data as CSV file. :point_right: ")
                with col2:
                    st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="data.csv",
                    mime="text/csv",
                )
                st.dataframe(data)
            except AttributeError:
                st.write(data)
        with tab2:
            st.write("## Plots :chart_with_upwards_trend:")
            try:
                viz_data = data.loc[:,['Year','Value','Country','Indicator']]
                indicators_in_data = viz_data['Indicator'].unique()
                for i, ind in enumerate(indicators_in_data):
                    st.write(f"### {indicator[i]} - over time")
                    
                    viz = viz_data[viz_data['Indicator'] == ind].loc[:,['Value','Year','Country']]
                    # viz['Year'] = viz['Year'].apply(lambda x: datetime.datetime.strptime(x, '%Y').strftime('%Y'))
                    
                    st.line_chart(viz,x='Year',y='Value',color='Country', use_container_width=True)
            except AttributeError:
                st.write('### Nothing to show :worried:')
    else:
        st.write("## No data to display.")

if __name__ == "__main__":
    main()