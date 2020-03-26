import GetData
import plotly.express as px
from plotly.offline import plot

COL_REGION = 'Country/Region'

df_cases_world = GetData.get_frame('confirmed')
LAST_DATE_I, dt_cols = GetData.get_dates(df_cases_world)

dt_today = dt_cols[LAST_DATE_I]
df_cases_world_group = df_cases_world.groupby(COL_REGION).sum()
df_cases_world_group.drop(['Lat', 'Long'], axis = 1, inplace = True)
df_cases_world_group.reset_index(inplace = True)
df_cases_world_group.rename(columns={COL_REGION:'country'}, inplace = True)

df_tmp = px.data.gapminder().query("year==2007")
df_tmp.drop(['year', 'lifeExp', 'pop', 'gdpPercap', 'iso_num'], axis = 1, inplace = True)

df_final = df_cases_world_group.merge(df_tmp, on = 'country')

#fig = px.scatter_geo(df_final, locations="iso_alpha", color="continent",
#                     hover_name="country", size="Confirmed",
#                     projection="natural earth")
#plot(fig)

