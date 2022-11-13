# add to 

def plot_categorical_and_continuous_vars(df, cat_vars_list, cont_vars_list):
    
    for col in cat_vars_list:
        for col2 in cont_vars_list:
            fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(16,6))
            fig.suptitle(f'{col} vs. {col2}')
            sns.boxplot(data=df, x=col, y=col2, ax=ax1)
            sns.violinplot(data=df, x=col, y=col2, ax=ax2)
            sns.barplot(data=df, x=col, y=col2, ax=ax3)
            plt.show()
            
            
def plot_variable_pairs_2(df, target):
    cols = df.columns.to_list()
    cols.remove(target)
    
    for col in cols:
        sns.lmplot(data= df, x=col, y=target, line_kws={'color':'red'})
    
    plt.show()
    
    
    
def plot_variable_pairs(df, target):
    cols = df.columns.to_list()
    cols.remove(target)
    
    for col in cols:
        sns.lmplot(data= df, x=col, y=target, line_kws={'color':'red'})
    
    plt.show()