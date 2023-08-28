import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np

######### this function to read data using path of data in your computer ##########
def loadDataFromPC(path):
    try:
        _, file_extension = os.path.splitext(path)
        
        if file_extension == ".csv":
            data = pd.read_csv(path)
        elif file_extension == ".xls":
            data = pd.read_excel(path)
        elif file_extension == ".xlsx":
            data = pd.read_excel(path)
        else:
            raise ValueError("Unsupported file format. Only CSV, XLSX, and XLS are supported.")

        return data
    
    except Exception as e:
        print("An error occurred while loading the data:", str(e))
        return None
    

def dataPreprosessing(data):
    for column in data.columns:
        nan_count = data[column].isna().sum()
        if nan_count > 3000:
            data.drop(column, axis=1, inplace=True)

    features = ['room_type','price','number_of_reviews','reviews_per_month','availability_365'] 

    data = data[features]       

    ## solve all nan data 
    df = pd.DataFrame(data)

    # Separate columns into numerical and categorical
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=[object]).columns

    # Fill missing values for numerical columns with mean
    for col in numerical_cols:
        df[col].fillna(df[col].mean(), inplace=True)

    # Fill missing values for categorical columns with mode
    for col in categorical_cols:
        mode_value = df[col].mode()[0]  # Get the most frequent value
        df[col].fillna(mode_value, inplace=True)
    
    return data

                



def displayHistogram(data,colName):
    count=data[colName].value_counts()
    # Generate random colors for each category
    num_categories = len(count)
    colors = [f'#%06X' % random.randint(0, 0xFFFFFF) for _ in range(num_categories)]

    plt.bar(count.index, count.values, color=colors)
    plt.title('{colName} Distribution Histogram')
    plt.xlabel(colName)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()


def displayviolinPlot(data):
    df = pd.DataFrame(data)
    # Create a combined countplot and box plot
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 10))

    ax = sns.countplot(x='room_type', data=df)
    ax2 = ax.twinx()  # Create a twin Axes sharing the xaxis

    sns.violinplot(x='room_type', y='price', data=df, ax=ax2)

    # Display the count on the bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=12, color='gray', xytext=(0, 10),
                    textcoords='offset points')

    ax.set_ylabel('Number of Occurrences')
    ax2.set_ylabel('Price')
    plt.title('Room Type, Price Distribution, and Counts')
    plt.show()



def displayboxPlot(data):
    df = pd.DataFrame(data)
    # Create a combined countplot and box plot
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 10))

    ax = sns.countplot(x='room_type', data=df)
    ax2 = ax.twinx()  # Create a twin Axes sharing the xaxis

    sns.boxplot(x='room_type', y='price', data=df, ax=ax2)

    # Display the count on the bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=12, color='gray', xytext=(0, 10),
                    textcoords='offset points')

    ax.set_ylabel('Number of Occurrences')
    ax2.set_ylabel('availability')
    plt.title('Room Type, Price Distribution, and Counts')
    plt.show()



def displayPiechart(data, column):
   
    count = data[column].value_counts()
    labels = count.index
    counts = count.values
    plt.figure(figsize=(8, 6))
    plt.pie(counts,labels=labels,autopct="%1.1f%%",startangle=90,colors=sns.color_palette("Set3"),)
    legend_labels = [f"{label} ({count})" for label, count in zip(labels, counts)]
    plt.legend(legend_labels, loc="best")
    plt.axis("equal")
    plt.title(f"{column} Pie Chart")
    plt.show()

def main():
    try:
        print()
        dataInput=input('Enter the data path here : ')
        data = loadDataFromPC(dataInput)
        dataProcessed = dataPreprosessing(data)
        ##print(data.head())
        while True:
            print('Press button [1] to see the result of data analysis using Histogram.')
            print('Press button [2] to see the result of data analysis using violinPlot.')
            print('Press button [3] to see the result of data analysis using boxPlot.')
            print('Press button [4] to see the result of data analysis using Piechart.')
            print('Press button [0] to Exit the system.')
            x=input('Your choice is : ')
            if(x == '1'):
                displayHistogram(dataProcessed,'room_type')
                print("\n\n\nAfter analyzing the distribution histogram, it becomes evident that "
                    "the category 'Entire home/apt' is the most predominant. Consequently, "
                    "in order to enhance our services, we should focus on offering an "
                    "increased number of listings of this particular type.\n\n\n")
            elif(x == '2'):
                displayviolinPlot(dataProcessed)
                print("\n\n\nIn our dataset, there is a higher number of entire home/apartment listings, often associated with higher prices. "
                    "To achieve a balance, we could lower the prices for some of these listings while increasing prices "
                    "for hotel rooms and shared rooms.\n\n\n")
            elif(x == '3'):
                displayboxPlot(dataProcessed)
                print("\n\n\nIn our dataset, there is a higher number of entire home/apartment listings, often associated with higher availability. "
                    "To achieve a balance, we could lower the prices for some of these listings while increasing prices "
                    "for hotel rooms and shared rooms.\n\n\n")
            elif(x == '4'):
                displayPiechart(dataProcessed,'room_type')
                print("\n\n\nAfter analyzing the distribution histogram, it becomes evident that "
                    "the category 'Entire home/apt' is the most predominant. Consequently, "
                    "in order to enhance our services, we should focus on offering an "
                    "increased number of listings of this particular type.\n\n\n")
            elif(x=='0'):
                print('Thank you for your time :).')
                break
            else:
                print('Please enter the available buttons only [1-2-3-4-0]')  
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")




if __name__ == "__main__":
    main()