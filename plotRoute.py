import pandas as pd
import matplotlib.pyplot as plt


def get_coordinates_dframe(instance):
    num_of_cust = instance['Number_of_customers']
    # Getting all customer coordinates
    customer_list = [i for i in range(1, num_of_cust + 1)]
    x_coord_cust = [instance[f'customer_{i}']['coordinates']['x'] for i in customer_list]
    y_coord_cust = [instance[f'customer_{i}']['coordinates']['y'] for i in customer_list]
    # Getting depot x,y coordinates
    depot_x = [instance['depart']['coordinates']['x']]
    depot_y = [instance['depart']['coordinates']['y']]
    # Adding depot details
    customer_list = [0] + customer_list
    x_coord_cust = depot_x + x_coord_cust
    y_coord_cust = depot_y + y_coord_cust
    df = pd.DataFrame({"X": x_coord_cust,
                       "Y": y_coord_cust,
                       "customer_list": customer_list
                       })
    return df

def plot_subroute(subroute, dfhere,color):
    totalSubroute = [0]+subroute+[0]
    subroutelen = len(subroute)
    for i in range(subroutelen+1):
        firstcust = totalSubroute[0]
        secondcust = totalSubroute[1]
        plt.plot([dfhere.X[firstcust], dfhere.X[secondcust]],
                 [dfhere.Y[firstcust], dfhere.Y[secondcust]], c=color)
        totalSubroute.pop(0)


def plot_route(subroutes, instance, title):
    colorslist = ["blue","green","red","cyan","magenta","yellow","black","#eeefff"]
    colorindex = 0

    # getting df
    dfhere = get_coordinates_dframe(instance)

    # Plotting scatter
    plt.figure(figsize=(10, 10))

    for i in range(dfhere.shape[0]):
        if i == 0:
            plt.scatter(dfhere.X[i], dfhere.Y[i], c='green', s=200)
            plt.text(dfhere.X[i], dfhere.Y[i], "depot", fontsize=12)
        else:
            plt.scatter(dfhere.X[i], dfhere.Y[i], c='orange', s=200)
            plt.text(dfhere.X[i], dfhere.Y[i], f'{i}', fontsize=12)

    # Plotting routes
    for route in subroutes:
        plot_subroute(route, dfhere, color=colorslist[colorindex])
        colorindex += 1

    # Plotting is done, adding labels, Title
    plt.xlabel("X - Coordinate")
    plt.ylabel("Y - Coordinate")
    plt.title(title)
    plt.savefig("figure/route.png")