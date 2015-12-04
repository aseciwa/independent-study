from tweet_preprocess import load_df

from textblob import TextBlob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import cartopy

# set graph display options 
pd.set_option('display.max_colwidth', 200)
pd.options.display.mpl_style = 'default'
matplotlib.style.use('ggplot')
sns.set_context('talk')
sns.set_style('darkgrid')

# load captured tweets
df = load_df('/Users/alanseciwa/Desktop/results3.csv')

# See the overall count relating to the keys 
df.info()

# prints out first row from tweets
print(df[['candidate', 'created_at', 'lang', 'place', 'user_followers_count', 
    'user_time_zone', 'polarity', 'influenced_polarity', 'text']].head(1))

# find polarity of ONLY english words and display the set
# the textblob function translate() could be used
english_df = df[df.lang == 'en']
english_df.sort('polarity', ascending=False).head(3)[['candidate', 'polarity', 'subjectivity', 'text']]

# Find mean polarity for each candidate by looking at the influenced_polarity. 
# this takes into account the number of retweets and number of followers
candidate_group = english_df.groupby('candidate')
print(candidate_group[['polarity', 'influence', 'influenced_polarity']].mean())

# Look at the influential Tweets about Donald Trump and Bernie Sanders
'''
jeb = candidate_group.get_group('Jeb Bush')
jeb_influence = jeb.sort('influence', ascending=False)
print('')
print('-----------')
print('Jeb Bush')
print('-----------')
print(jeb_influence[['influence', 'polarity', 'influenced_polarity', 'user_name', 'text', 'created_at']].head(5))

print('')
print('-----------')
print(df[df.user_name == 'Jeb Bush'].groupby('candidate').size())
'''
# Trump
trump = candidate_group.get_group('Donald Trump')
trump_influence = trump.sort('influence', ascending=False)
print('--------------')
print('Donald Trump')
print('--------------')
trump_influence[['influence', 'polarity', 'influenced_polarity', 'user_name', 'text', 'created_at']].head(5)


# Sanders
sanders = candidate_group.get_group('Bernie Sanders')
sanders_influence = sanders.sort('influence', ascending=False)
print('--------------')
print('Bernie Sanders')
print('--------------')
sanders_influence[['influence', 'polarity', 'influenced_polarity', 'user_name', 'text', 'created_at']].head(5)

# LANGUAGE
# display who are all twitter from different languages
print('')
print('Language')
lang_group = df.groupby(['candidate', 'lang'])
print(lang_group.size())

# graph the languages
print('')
l_lang = lang_group.filter(lambda group: len(group) > 10)

# get rid of english language
non_eng = l_lang[l_lang.lang != 'en']
non_eng_grp = non_eng.groupby(['lang', 'candidate'], as_index = False)
non_eng_grp

print('')
print('ploting...')
s = non_eng_grp.text.agg(np.size)
s = s.rename(columns={'text': 'count'})
s_pivot_dis = s.pivot_table(index='lang', columns='candidate', values='count', fill_value=0)

plot = sns.heatmap(s_pivot_dis)
plot.set_title('Number of non-English Tweets by Candidate')
plot.set_ylabel('language code')
plot.set_xlabel('candidate')
plot.figure.set_size_inches(12, 7)
print('')
print('ending plotting')

# Time-influence polarity over time for each candidate
mean_pol = df.groupby(['candidate', 'created_at']).influenced_polarity.mean()
plot = mean_pol.unstack('candidate').resample('60min').plot()
plot.set_title('Influence Polarity Over Time for Candidates')
plot.set_ylabel('Influence Polarity')
plot.set_xlabel('Time')
plot.figure.set_size_inches(15, 9)

# Get top languages
lang_size =df.groupby('lang').size()
th = lang_size.quantile(.75)

top_lang_df = lang_size[lang_size > th]
top_lang = set(top_lang_df.index) - {'und'}
print(top_lang)

# Get tweet frequency
df['hour'] = df.created_at.apply(lambda datetime: datetime.hour)

for lang_code in top_lang:
    l_df = df[df.lang == lang_code]
    normalized_freq = l_df.groupby('hour').size() / l_df.lang.count()
    plot = normalized_freq.plot(label = lang_code)
    
plot.set_title('Tweet Frequency by hour of day')
plot.set_ylabel('frequency')
plot.set_xlabel('hr of day')
plot.legend()
plot.figure.set_size_inches(10, 8)

# find the uniqueness of tweets
spike_interest = df[(df.hour == 23) & (df.lang == 'in')]

print('Number of tweets:', spike_interest.text.count())
print('Number of unique users:', spike_interest.user_name.unique().size)

#investigate spike from Indonesia
spike_interest.text.head(10).unique()

# Find the Timezone of tweets in different locations with Influenced_Polarity
timez_df = english_df.dropna(subset=['user_time_zone'])
us_timez_df = timez_df[timez_df.user_time_zone.str.contains('US & Canada')]
us_timez_candidate_group = us_timez_df.groupby(['candidate', 'user_time_zone'])
us_timez_candidate_group.influenced_polarity.mean()

# Graph timezone on a map
timez_map = cartopy.io.shapereader.Reader("/Users/alanseciwa/Desktop/World_Maps/tz_world_mp.shp")
timez_rec = list(timez_map.records())
timez_trans = {
    'Eastern Time (US & Canada)': 'America/New_York',
    'Central Time (US & Canada)': 'America/Chicago',
    'Mountain Time (US & Canada)': 'America/Denver',
    'Pacific Time (US & Canada)': 'America/Los_Angeles',
}
america_timez_rec = {
    timez_name: next(filter(lambda record: record.attributes['TZID'] == timez_id, timez_rec))
    for timez_name, timez_id 
    in timez_trans.items()
}

# -----
aea = cartopy.crs.AlbersEqualArea(-95, 35)
pc = cartopy.crs.PlateCarree()

state_province = cartopy.feature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none'
) 

c_map = [matplotlib.cm.Blues, matplotlib.cm.Greens, matplotlib.cm.Reds, matplotlib.cm.Oranges]
norm = matplotlib.colors.Normalize(vmin=0, vmax=40)

candidates = df['candidate'].unique()

for i, c in enumerate(candidates):
    plt.figure()
    plot = plt.axes(projection=aea)
    plot.set_extent((-125, -66, 20, 50))
    plot.add_feature(cartopy.feature.LAND)
    plot.add_feature(cartopy.feature.COASTLINE)
    plot.add_feature(cartopy.feature.BORDERS)
    plot.add_feature(state_province, edgecolor='gray')
    plot.add_feature(cartopy.feature.LAKES, facecolor='#00BCD4')
    
    for j, r in america_timez_rec.items():
        timez_spec_df = us_timez_df[us_timez_df.user_time_zone == j]
        timez_cand_spec_df = timez_spec_df[timez_spec_df.candidate == c]
        mean_pol = timez_cand_spec_df.influenced_polarity.mean()
        
        plot.add_geometries(
            [r.geometry],
            crs = pc, 
            color = c_map[i](norm(mean_pol)),
            alpha = 0.8
        )
    
    plot.set_title('Influenced Polarity towards {} by U.S. Timezone'.format(c))
    plot.figure.set_size_inches(7, 4)
    plt.show()
    print() 
        
# Find the Twitter users outside of the U.S. 
american_timez = ('US & Canada|Canada|Arizona|America|Hawaii|Indiana|Alaska'
                    '|New_York|Chicago|Los_Angeles|Detroit|CST|PST|EST|MST')

foreign_timez_df = timez_df[~timez_df.user_time_zone.str.contains(american_timez)]
foreign_timez_grp = foreign_timez_df.groupby('user_time_zone')
foreign_timez_grp.size().sort(inplace=False, ascending=False).head(25)

# find Foreign timezones and influenced_polarity of candidates
foreign_english_timez_df = foreign_timez_df[foreign_timez_df.lang == 'en']

foreign_timez_grp2 = foreign_english_timez_df.groupby(['candidate', 'user_time_zone'])
top_foreign_timez_df = foreign_timez_grp2.filter(lambda group: len(group) > 40)

top_foreign_timez_grp = top_foreign_timez_df.groupby(['user_time_zone', 'candidate'], as_index=False)

mean_infl_pol = top_foreign_timez_grp.influenced_polarity.mean()

pivot = mean_infl_pol.pivot_table(
    index='user_time_zone', 
    columns='candidate', 
    values='influenced_polarity',
    fill_value=0
)

plot = sns.heatmap(pivot)
plot.set_title('Influenced Polarity in Major Foreign (timezones) Regions by Candidate')
plot.set_ylabel('City', family='Ubuntu')
plot.set_xlabel('Influenced Polarity by Candidate')
plot.figure.set_size_inches(10, 9)

# Find the Geolocation of Tweets made
geo_df = df.dropna(subset=['place'])
mollweide = cartopy.crs.Mollweide()

plot = plt.axes(projection=mollweide)
plot.set_global()
plot.add_feature(cartopy.feature.LAND)
plot.add_feature(cartopy.feature.COASTLINE)
plot.add_feature(cartopy.feature.BORDERS)

plot.scatter(
    list(geo_df.longitude), 
    list(geo_df.latitude), 
    transform=pc, 
    zorder=2
)

plot.set_title('International Twitter Users W/Enabled Geo Data')
plot.figure.set_size_inches(14, 9)

# Plot Twitter user in the US
plot = plt.axes(projection=aea)

## this set the size of the map. If other portions of the 
## map need to be accessed, the these coordinates
plot.set_extent((-150, 60, -25, 60))

# <fix> need to fix, state border lines are not showing
plot.add_feature(state_province, edgecolor='black')
plot.add_feature(cartopy.feature.COASTLINE)
plot.add_feature(cartopy.feature.LAND)
plot.add_feature(cartopy.feature.BORDERS)
plot.add_feature(cartopy.feature.LAKES)

candidate_grp2 = geo_df.groupby('candidate', as_index = False)

# Colors for the legend table
colors = ['#DC143C', '#0000FF', '#FFD700', '#9932CC']

# Go through loop to display the coordinates 
for i, (can, grp) in enumerate(candidate_grp2):
    longitudes = grp.longitude.values
    latitudes = grp.latitude.values
    plot.scatter(
        longitudes, 
        latitudes, 
        transform=pc, 
        color=colors[i], 
        label=can,
        zorder=2
    )
plot.set_title('Twitter Users by Candidate')
plt.legend(loc='lower right')
plot.figure.set_size_inches(12, 7)