import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline #only for the if name=main
from sklearn.compose import ColumnTransformer #only for the if name=main
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler #only for the if name=main

### class Segmentation :
###   input :
###      you need to give the encoded df WITHOUT the customer_ID colomn
###      and the customer_ID on a separate df
###   output :
###      return a df with 2 rows, the customer_ID (unique) and the segmentation categorie
###
###
### To use this class :
###   
###   1. init the class 
###        segmentation = Segmentation( <encoded_df> , <customer_ID_df> )
###
###   2. fit the class
###        segmentation.fit()
###
###   3. predict the class return a df with two columns
###        final_df = segmentation.predict()


class Segmentation():
    
    def __init__(self, data_df, customer_ID_df):
        self.data_df = data_df
        self.customer_ID_df = customer_ID_df
        
    #### For later ... need to find a way to predict the perfect k dynamicaly. we will take 10 for now
    
    # def k_finder(self):
    #     # inertias = []
    #     # ks = range(1,50,2)
    #     # for k in ks:
    #     #     km_test = KMeans(n_clusters=k).fit(X_train_transformed)
    #     #     inertias.append(km_test.inertia_)
    #     self.n_cluster=10
    #     return self.n_cluster
    
    def fit(self,n_cluster=10):

        # doing the kmeans model
        km = KMeans(n_clusters=n_cluster)
        km.fit(self.data_df)

        # returning the segmntation df with ID (one customer_ID can epear many times)
        customer_segmentation_list = km.labels_.tolist()
        self.customer_ID_df['segmentation'] = customer_segmentation_list
        return self.customer_ID_df
    
    def predict(self):
        # creating empty list to creat the final DF with unique customer_ID
        seg = []
        cust = []

        # feeding the list with the most commun segmentation for every unique customer_ID
        for customer in self.customer_ID_df['customer_ID'].unique():
            tmp_df = self.customer_ID_df[self.customer_ID_df['customer_ID'] == customer]
            seg.append(tmp_df['segmentation'].mode()[0])
            cust.append(customer)

        # creating and returning the segmntation df with ID (one customer_ID epears only one times)
        self.segment_df = pd.DataFrame({"customer_ID": cust, "customer_segmentation": seg})
        return self.segment_df
       
    
    
    
if __name__ == "__main__":

    # loading the df
    data_df = pd.read_csv('data/data_400_000_rows_clean_df.csv')
    data_df = data_df.sample(2000)

    # puting the customer_ID on a side
    customer_segmentation_df = data_df[['customer_ID']]

    # doing the encoding
    X_train = data_df[['price', 'vendor', 'product_cat', 'gender', 'quantity' , 'final_price',
                       'product_gender']]
    cat_transformer = OneHotEncoder(handle_unknown='ignore',sparse = False)
    num_transformer = MinMaxScaler()

    preprocessor = ColumnTransformer([
        ('num_tr_Minmax', num_transformer, ['price','price','final_price']),
        ('cat_tr', cat_transformer, ['vendor', 'product_cat', 'gender','product_gender'])],
        remainder= 'passthrough')

    X_train_transformed = preprocessor.fit_transform(X_train)

    # init the class
    segmentation=Segmentation(X_train_transformed,customer_segmentation_df)

    # fit the class
    segmentation.fit()

    # predict the class
    final_df = segmentation.predict()
    print(final_df)