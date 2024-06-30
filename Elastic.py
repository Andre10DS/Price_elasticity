import pandas            as pd
import numpy             as np
import statsmodels.api   as sm
import streamlit         as st
from   io                import StringIO
import inflection


st.set_page_config(layout='wide')

# Upload the data
def get_data(path):
    data=pd.read_csv(path)
    #data = data.loc[data['merchant'] == 'Bestbuy.com']
    return data

# Adjust column headings
def column_adjustment(data):

    cols_old = ['Unnamed: 0', 'Date_imp', 'Date_imp_d', 'Cluster', 'Category_name',
        'name', 'price', 'disc_price', 'merchant', 'condition',
        'Disc_percentage', 'isSale', 'Imp_count', 'brand', 'p_description',
        'currency', 'dateAdded', 'dateSeen', 'dateUpdated', 'imageURLs',
        'manufacturer', 'shipping', 'sourceURLs', 'weight', 'Date_imp_d.1',
        'Day_n', 'month', 'month_n', 'day', 'Week_Number', 'Zscore_1',
        'price_std']

    snakecase = lambda x: inflection.underscore(x)
    cols_new = list( map(snakecase, cols_old) )

    data.columns = cols_new


    data = data.drop(columns=['unnamed: 0', 'date_imp', 'cluster', 'condition',
                       'disc_percentage', 'is_sale', 'imp_count', 'p_description',
                       'currency', 'date_added', 'date_seen', 'date_updated', 'image_ur_ls',
                       'shipping', 'source_ur_ls', 'weight', 'date_imp_d.1', 'zscore_1',
                       'price_std'])
    
    return data

# Change Data Type

def change_type(data):
    #Change types
    data['date_imp_d'] = pd.to_datetime(data['date_imp_d'])

    return data

# Category and Company Selection

def select_and_replace_data(data):

# Select data


    
    st.sidebar.title('Select enterprise and category')

    enterprisename = data['merchant'].unique().tolist()

    f_enterprise = st.sidebar.selectbox('Enter enterprise', enterprisename,index=enterprisename.index('Bestbuy.com') if 'Bestbuy.com' in enterprisename else 0)

    df_0 = data[data['merchant'] == f_enterprise]

    categoryname = df_0['category_name'].unique().tolist()
    
    f_category = st.sidebar.selectbox('Enter category', categoryname,index=categoryname.index('laptop, computer') if 'laptop, computer' in categoryname else 0, key="select")

    df_1 = df_0[df_0['category_name'] == f_category]

    
    test = df_1.groupby(['name','week_number']).agg({'disc_price':'mean', 'date_imp_d':'count'}).reset_index()

    x_price = test.pivot(index='week_number', columns='name', values='disc_price')
    x_price = pd.DataFrame(x_price.to_records())

    y_demand = test.pivot(index='week_number', columns='name', values='date_imp_d')
    y_demand = pd.DataFrame(y_demand.to_records())

# Replace NA
    median_price = np.round(x_price.median(),2)
    x_price.fillna(median_price, inplace=True)
   
    y_demand.fillna(0, inplace=True)

    return x_price, y_demand

# Creating the Price Elasticity Table
def table(data_x,data_y):
    results_values_category = {
        'name': [],
        'price_elasticity': [],
        'price_mean': [],
        'quantity_mean': [],
        'intercept': [],
        'slope': [],
        'rsquared': [],
        'p_value': []
     }

    for column in data_x.columns[1:]:
        column_points = []
        for i in range(len(data_x[column])):
            column_points.append((data_x[column][i],data_y[column][i]))
        df = pd.DataFrame(list(column_points), columns=['x_price', 'y_demand'])
        x_laptop = df['x_price']
        y_laptop = df['y_demand']
        x_laptop = sm.add_constant(x_laptop)
        model = sm.OLS(y_laptop, x_laptop)
        results = model.fit()
        
        if results.f_pvalue < 0.05:
            
            rsquared = results.rsquared
            p_value = results.f_pvalue
            intercept, slope = results.params
            mean_price = np.mean(x_laptop)
            mean_quantity = np.mean(y_laptop)
            price_elasticity = slope*( mean_price / mean_quantity)

            results_values_category['name'].append(column)
            results_values_category['price_elasticity'].append(price_elasticity)
            results_values_category['price_mean'].append(mean_price)
            results_values_category['quantity_mean'].append(mean_quantity)
            results_values_category['intercept'].append(intercept)
            results_values_category['slope'].append(slope)
            results_values_category['rsquared'].append(rsquared)
            results_values_category['p_value'].append(p_value)
        

    df_elasticity = pd.DataFrame.from_dict(results_values_category)
    return df_elasticity

# Elasticity ranking

def ranking_elastic(data):
    data['ranking'] = data.loc[:, 'price_elasticity'].rank(ascending=True).astype(int)
    data = data.reset_index(drop=True)
    df_order = data[['ranking', 'name', 'price_elasticity']].sort_values(by='price_elasticity', ascending=False)
    return df_order
 
# Creation of the Elasticity Impact Table
      
def Business_per(data, data_x, data_y, op, number):



    if op =='increase':

        per_var = (100 + number)/100
        num_var = 100 + number
        per_elast = (100 - num_var)/100


        result_faturamento = {
        'name': [],
        'faturamento_atual': [],
        #'faturamento_reducao': [],
        #'perda_faturamento': [],
        'faturamento_novo': [],
        'variacao_faturamento': [],
        'variacao_percentual': []
    
        }
    


        for i in range( len(data)):
            preco_atual_medio = data_x[data['name'][i]].mean()
            demanda_atual = data_y[data['name'][i]].sum()


            reducao_preco = preco_atual_medio * per_var



            #aumento_demanda = abs(per_elast * data['price_elasticity'][i])
            aumento_demanda = -1*per_elast * data['price_elasticity'][i]


            demanda_nova = aumento_demanda * demanda_atual


            faturamento_atual = round(preco_atual_medio*demanda_atual, 2)
            faturamento_novo = reducao_preco*demanda_nova
        
           # faturamento_reducao = round(faturamento_atual*per_var, 2)
        
           # perda_faturamento = round(faturamento_atual-faturamento_novo, 2)
        
            variacao_faturamento = round(faturamento_novo - faturamento_atual, 2)    
        
            variacao_percentual = round(((faturamento_novo - faturamento_atual)/faturamento_atual)*100, 2)
        
            result_faturamento['name'].append(data['name'][i])
            result_faturamento['faturamento_atual'].append(faturamento_atual)
           # result_faturamento['faturamento_reducao'].append(faturamento_reducao)
           # result_faturamento['perda_faturamento'].append(perda_faturamento)
            result_faturamento['faturamento_novo'].append(faturamento_novo)
            result_faturamento['variacao_faturamento'].append(variacao_faturamento)
            result_faturamento['variacao_percentual'].append(variacao_percentual)

            result_var = pd.DataFrame(result_faturamento)

    else:

        per_var = (100 - number)/100
        num_var = 100 - number
        per_elast = (100 - num_var)/100


        result_faturamento = {
            'name': [],
            'faturamento_atual': [],
            #'faturamento_reducao': [],
            #'perda_faturamento': [],
            'faturamento_novo': [],
            'variacao_faturamento': [],
            'variacao_percentual': []
        
            }
    


        for i in range( len(data)):
            preco_atual_medio = data_x[data['name'][i]].mean()
            demanda_atual = data_y[data['name'][i]].sum()


            reducao_preco = preco_atual_medio * per_var


            #aumento_demanda = abs(per_elast * data['price_elasticity'][i])
            aumento_demanda = -1 * per_elast * data['price_elasticity'][i]


            demanda_nova = aumento_demanda * demanda_atual

        
            faturamento_atual = round(preco_atual_medio*demanda_atual, 2)
            faturamento_novo = reducao_preco*demanda_nova
        
            #faturamento_reducao = round(faturamento_atual*per_var, 2)
        
            #perda_faturamento = round(faturamento_atual-faturamento_novo, 2)
        
            variacao_faturamento = round(faturamento_novo - faturamento_atual, 2)    
        
            variacao_percentual = round(((faturamento_novo - faturamento_atual)/faturamento_atual)*100, 2)
        
            result_faturamento['name'].append(data['name'][i])
            result_faturamento['faturamento_atual'].append(faturamento_atual)
            #result_faturamento['faturamento_reducao'].append(faturamento_reducao)
            #result_faturamento['perda_faturamento'].append(perda_faturamento)
            result_faturamento['faturamento_novo'].append(faturamento_novo)
            result_faturamento['variacao_faturamento'].append(variacao_faturamento)
            result_faturamento['variacao_percentual'].append(variacao_percentual)

            result_var = pd.DataFrame(result_faturamento)
        
    return result_var


if __name__ == '__main__':
  
    #Data extraction
    path = 'data/raw/df_ready.csv'

    data = get_data(path)
    data = column_adjustment(data)
    data = change_type(data)
    data_x, data_y = select_and_replace_data(data)
    elastic = table(data_x, data_y)
    base_business = ranking_elastic(elastic)
    

    tab1, tab2 = st.tabs(['Price Elasticity', 'Scenarios'])

    with tab1:
        st.write("## Category Price Elasticity")
    
        st.dataframe(elastic)

    with tab2:
                
        col1, col2 = st.columns((1,1))

        with col1:
            
            st.markdown("<h2 style='text-align: center;'>Apply a discount or a price increase?</h2>", unsafe_allow_html=True)
            option = st.selectbox(
            '',
            ('Price Increase', 'Apply Discount'))
            if option == 'Price Increase':
                op = 'increase'
            else:
                op = 'discount'

        with col2:
            
            st.markdown('<h2 style="text-align: center;">Percentage of '+op+' do you want to apply?</h2>', unsafe_allow_html=True)
            number = st.number_input('', min_value=0., max_value=100.0, step=0.1)
        
        result_perfor = Business_per(base_business, data_x, data_y, op, number)
        st.dataframe(result_perfor)
            