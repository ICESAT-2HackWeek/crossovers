def plot_ATL06(data, attribute = None, filtered = False):
    """
    Plots the provided ATL06 tracks by longitude and latitude. If an attribute is provided, the points data is colored 
    according to the specified attribute. Data can also be filtered to remove low-quality data
    Parameters
    ___________
    data: dataframe 
    ATL06 tracks to be plotted
    
    attribute(optional): string
    attribute to use for the colorbar. If no attribute is selected, all points will be plotted in black
    
    filtered: boolean
    specifies wether you want to filter out low-quality data (indicated by a quality_summary value of 1)
    
    Returns
    _________+
    none
    """
    fig = plt.figure(figsize = (10, 10));
    
    if filtered:
        data_f = data.loc[data['atl06_quality_summary'] == 0] #keep only high quality data
    else:
          data_f = data  
    if attribute is None:
        plt.scatter(data_f['longitude'], data_f['latitude'], c = 'k', s =0.0001) #plot data in black
    else:
        plt.scatter(data_f['longitude'], data_f['latitude'], c = data_f[attribute], s =0.0001) #plot data colored by attribute
        cbar = plt.colorbar() #add colorbar
        cbar.set_label(attribute, rotation = 270)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
def select_crossover(data, lons, lats, attribute = None, filtered = False):
    """
    Filters the provided dataframe based on the provided bounding lon.lat values and highlights the selction on the 
    full data plot map
    Parameters:
    ___________
    data: dataframe 
    dataframe with ATL06 track data
    
    lons: list
    list of minimum and maximum longitude
    
    lats: list
    list of minimum and maximum longitudes
    
    attribute:
    see plot_ATL06
    
    filtered:
    see plot_ATL06
    
    Returns
    __________
    ATL06_filtered: dataframe
    A filtered dataframe conatining only the data in the specified lon/lat range
    """
    %matplotlib inline
    plot_ATL06(data, attribute = attribute, filtered = filtered) #make plot of full data
    #draw bounding box:
    plt.plot([lons[0], lons[0]], [lats[0], lats[1]], 'r')
    plt.plot([lons[1], lons[1]], [lats[0], lats[1]], 'r')
    plt.plot([lons[0], lons[1]], [lats[0], lats[0]], 'r')
    plt.plot([lons[0], lons[1]], [lats[1], lats[1]], 'r')
    
    ATL06_filtered = data.loc[((data['latitude'] < lats[1]) & (data['latitude'] > lats[0]) )& (\
                           (data['longitude'] < lons[1]) & (data['longitude'] > lons[0]))] #filter the data
    return ATL06_filtered

def plot_crossovers_3d(ATL06_filtered, rgt_list = None):
    """
    Makes a 3-d elevation plot of specified tracks in the provided dataframe
    
    Parameters
    __________
    ATL06_filtered: dataframe
    dataframe containing crossover tracks
    
    rgt_list: list
    list of rgt tracks to be plotted, if you only want to plot a subset of them. If no list is provided, all tracks
    will be plotted
    
    Returns
    ________
    none
    """
    %matplotlib notebook
    %matplotlib notebook
    fig = plt.figure(figsize = (10, 10))
    if rgt_list == None:
        rgts = ATL06_filtered['RGT'].unique() #get list of all RGTs in the dataset
    else:
        rgts = rgt_list
    ax = fig.add_subplot(111, projection = '3d') #initialize 3d plot
    colormap = plt.cm.hsv #define colormap
    colors = [colormap(i) for i in np.linspace(0, 0.99, len(rgt)*6+1)] #define a list of colors from the colormap - 1 for each indivdual beam (so 6 per ground track)
    i = 1 #start counter for color list
    for r in rgts:
        ATL06_r = ATL06_filtered.loc[(ATL06_filtered['RGT'] == r)]
        date = (ATL06_r['date'].values)[0] #extract the date for labeling
        #seperate the points for each beam in each pair
        gt1l = ATL06_filtered.loc[(ATL06_filtered['RGT'] == r) & (ATL06_filtered['p_b']== '1.0_0.0')]
        gt1r = ATL06_filtered.loc[(ATL06_filtered['RGT'] == r) & (ATL06_filtered['p_b']== '1.0_1.0')]
        gt2l = ATL06_filtered.loc[(ATL06_filtered['RGT'] == r) & (ATL06_filtered['p_b']== '2.0_0.0')]
        gt2r = ATL06_filtered.loc[(ATL06_filtered['RGT'] == r) & (ATL06_filtered['p_b']== '2.0_1.0')]
        gt3l = ATL06_filtered.loc[(ATL06_filtered['RGT'] == r) & (ATL06_filtered['p_b']== '3.0_0.0')]
        gt3r = ATL06_filtered.loc[(ATL06_filtered['RGT'] == r) & (ATL06_filtered['p_b']== '3.0_1.0')]
        
        #plot each beam with a different color:
        ax.scatter(gt1l['longitude'], gt1l['latitude'], gt1l['h_li'], c = [colors[1*i]] * len(gt1l),s = .5, \
                   label = ('gt1l' + str(date)[0:10]))
        ax.scatter(gt1r['longitude'], gt1r['latitude'], gt1r['h_li'], c = [colors[2*i]] * len(gt1r),s = .5,\
                   label = 'gt1r'+ str(date)[0:10])
        ax.scatter(gt2l['longitude'], gt2l['latitude'], gt2l['h_li'], c = [colors[3*i]] * len(gt2l),s = .5,\
                   label = 'gt2l' + str(date)[0:10])
        ax.scatter(gt2r['longitude'], gt2r['latitude'], gt2r['h_li'], c =[colors[4*i]] * len(gt2r),s = .5,\
                   label = 'gt2r'+str(date)[0:10])
        ax.scatter(gt3l['longitude'], gt3l['latitude'], gt3l['h_li'], c = [colors[5*i]] * len(gt3l),s = .5, \
                   label = 'gt3l' + str(date)[0:10])
        ax.scatter(gt3r['longitude'], gt3r['latitude'], gt3r['h_li'], c = [colors[6*i]] * len(gt3r),s = .5, \
                   label = 'gt3r'+ str(date)[0:10])
        i = i+1 #increment counter for color list
    ax.legend()
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_zlabel('elevation (m)')
    #set axis limits
    ax.set_xlim3d(np.min(ATL06_filtered['longitude'].values), np.max(ATL06_filtered['longitude'].values))
    ax.set_ylim3d(np.min(ATL06_filtered['latitude'].values), np.max(ATL06_filtered['latitude'].values))
    
def get_summary(ATL06_filtered):
    """
    provides a summary of a given subset of the data: what tracks are present, what dates they were measured, and 
    how many individula data point are present fior each one. The spatial extent is also included for reference.
    
    Parameters
    __________
    ATL06_filtered: dataframe to be summarized
    
    Returns:
    _________
    summary: dataframe
    a dataframe that list all RGTs in the dataset, along with their measurement date, number of measurements, and 
    the spatial extent covered.
    """
    rgts = ATL06_filtered['RGT'].unique() #get lst of RGTs
    extent = [[np.min(ATL06_filtered['longitude'].values), np.max(ATL06_filtered['longitude'].values)], [np.min(ATL06_filtered['latitude'].values), np.max(ATL06_filtered['latitude'].values)]]
    print(extent)
    num_points = [] #initialize list for the numb er of points in each RGT
    dates = [] #intitialize list for date of each RGT
    
    for r in rgts:
        rgt = ATL06_filtered.loc[ATL06_filtered['RGT'] == r] #filter for RGT
        num_points.append(len(rgt)) #count and store the number of data point for the given RGT
        dates.append(rgt['date'].values[0]) #append the date   
        #make summary:
    s = {'RGT': rgts, 'Date': dates, 'Number of points':num_points, 'Extent': [extent]*len(rgts)}
    summary = pd.DataFrame(data = s)
    return summary
