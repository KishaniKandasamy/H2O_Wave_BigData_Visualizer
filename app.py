from h2o_wave import app, ui, Q, main, data
from numpy.lib.twodim_base import tri
import pandas as pd

#page = site['/']


@app("/")
async def serve(q):
    if not q.client.initialized:
        setupfor_Newuser(q)
        table_view(q)
    elif q.args.table:
        table_view(q)
    elif q.args.plot:
        Plot_view(q)
    elif (q.args.x_variable is not None) or (q.args.y_variable is not None):
        q.client.x_variable = q.args.x_variable
        q.client.y_variable = q.args.y_variable
        Plot_view(q)
        

    await q.page.save()
    
    
    
def setupfor_Newuser(q): #set up header and navigation to new user
    q.page["meta"] = ui.meta_card(
        box="",
        layouts=[
            ui.layout(
                breakpoint="xs",
                zones=[ui.zone("header"), ui.zone("navigation"), ui.zone("content")],
            )
        ],
    )

    q.page['header1'] = ui.header_card(
            box="header",
            title="Aggregated Visualizer",
            subtitle="Allowing user to visualize larger database"
    )

    q.page["navigation"] = ui.tab_card(
            box="navigation",
            items=[
                ui.tab(name="table", label="Table View"),
                ui.tab(name="plot" , label="Plot View")
            ]
    )
    
    q.client.x_variable ='c1'
    
    q.client.y_variable ='c2'
    
    q.client.initialized=True
    
def table_view(q):
    del q.page["plotview"]
    
    df=aggregated_data()
    
    q.page["tableview"] = ui.form_card(
        box="content",
        items=[
            ui.text_xl("Table View"),
            ui.table(
                name='aggregated_data_table',
                columns=[
                    ui.table_column(name=col, label=col) for col in df.columns.values
                    ],
                rows=[
                    ui.table_row(
                        name=str(i),
                        cells=[str(df[col].values[i]) for col in df.columns.values]
                    ) for i in range(len(df))
                ],
                downloadable = True
            )
        ]
    )
    
def Plot_view(q):
    del q.page["tableview"]
    
    df=aggregated_data()
    
    q.page["plotview"] = ui.form_card(
        box="content",
        items=[
            ui.text_xl(f"Relationship between { q.client.x_variable }  and {q.client.y_variable}"),
            
            ui.inline(items=[
               
               ui.dropdown(
                     name='x_variable', 
                     label='X variable',
                     choices=[
                        ui.choice(name=col, label=col) for col in df.columns.values
                    ],
                     trigger= True,
                     value=q.client.x_variable 
                
                ),
                ui.dropdown(
                    name='y_variable', 
                    label='Y variable',
                    choices=[
                        ui.choice(name=col, label=col) for col in df.columns.values
                    ],
                    trigger=True,
                    value=q.client.y_variable 
                ),
            ]),
            
            
            ui.visualization(
                data=data(
                    fields=df.columns.tolist(),
                    rows=df.values.tolist(),
                    pack=True, #for static data(Not real time data)
                ),
                plot=ui.plot(marks=[ui.mark(
                    type='point',
                    x=f'={q.client.x_variable}', x_title='',
                    y=f'={q.client.y_variable}', y_title='',
                    color='red',shape='circle',size='=counts'
                )])
            )
        ]
    )
    
def aggregated_data():
    df= pd.DataFrame(dict(
        c1=range(0,100),
        c2=range(1, 101),
        counts=range(2,102)  
    ))
    return df


    