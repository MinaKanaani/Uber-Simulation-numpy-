import numpy as np


T = 150
req_num =100
users = np.array(
    [[1001, 1, 1], [1002, 1, 1], [1003, 0, 1], [1004, 1, 1], [1005, 1, 1], [1006, 1, 1], [1007, 0, 1], [1008, 1, 1],
     [1009, 0, 1], [1010, 1, 1],[1011, 1, 1], [1012, 1, 1], [1013, 1, 1], [1014, 1, 1], [1015, 1, 1], [1016, 1, 1],
     [1017, 1, 1], [1018, 1, 1], [1019, 0, 1], [1020, 1, 1], 
     [3001, 0, 0], [3002, 0, 0], [3003, 1, 0], [3004, 0, 0], [3005, 1, 0], [3006, 0, 0], [3007, 0, 0], [3008, 0, 0],
     [3009, 1, 0], [3010, 1, 0], [3011, 0, 0], [3012, 0, 0], [3013, 1, 0], [3014, 0, 0], [3015, 1, 0], [3016, 0, 0],
     [3017, 1, 0], [3018, 0, 0], [3019, 1, 0], [3020, 0, 0], [3021, 1, 0], [3022, 1, 0], [3023, 0, 0], [3024, 0, 0],
     [3025, 0, 0], [3026, 1, 0], [3027, 0, 0], [3028, 0, 0], [3029, 1, 0], [3030, 0, 0]])

drivers = np.column_stack(( np.arange(1001, 1021, 1), np.random.randint(1, 100, 20), np.random.randint(1, 100, 20),
     np.random.randint(0, 1, 20)))

trips = np.column_stack(
    (np.arange(11111, 11111 + req_num, 1), np.random.choice(users[users[:,0] > 1999][:, 0], req_num),
     np.sort(np.random.randint(1, T, req_num)), np.random.randint(1, 100, req_num),
     np.random.randint(1, 100, req_num), np.random.randint(1, 100, req_num), np.random.randint(1, 100, req_num)))
print(users)
print(drivers)
print(trips)
def distance(disttype,x1,x2,y1,y2):
    global Z
    if disttype==1:
        Z=np.sqrt((x2-x1)**2+(y2-y1)**2)
    elif disttype==0:
        Z=(abs(x2-x1)+abs(y2-y1))
    #print(Z)
def duration(Z):
    traffic_rate=np.sin(t/1000)*0.016+0.08
    global trip_time
    trip_time=np.ceil(Z*traffic_rate)
    #print(trip_time)
    
def payment(trip_time):
    global trip_payment
    payment_rate=np.ceil(np.cos(t/12))*50+200
    trip_payment=(payment_rate*trip_time)
    #print(trip_payment)

def alloc(disttype):
    
    global newtrips
    newtrips=np.insert(trips,7,0,axis=1)
    for i in range(req_num):
        
        access1=np.where(drivers[:,3]<trips[i,2])
        access2=np.asarray(access1)
        #print(access2)
        global accessible
        accessible=access2[0]
        #print(accessible)
        #print(drivers[accessible,0])
        if any(accessible):
            #print(access1)
            if disttype==1:
                min_dist=np.sqrt((drivers[accessible,1]-trips[i,3])**2+(drivers[accessible,2]-trips[i,4])**2)
            elif disttype==0:
                min_dist=abs(drivers[accessible,1]-trips[i,3])+abs(drivers[accessible,2]-trips[i,4])
            #print(min_dist)
            #print(np.argmin(min_dist))
            global proper_driver
            proper_driver=np.argmin(min_dist)
            #print(type(accessible))
            #print(drivers[accessible[proper_driver],0])
            driver_code=drivers[accessible[proper_driver],0]
            payment_time=int(trip_time[i]+trips[i,2])
            #print(payment_time)
            drivers[accessible[proper_driver],3]=payment_time
            drivers[accessible[proper_driver],1]=trips[i,5]
            drivers[accessible[proper_driver],2]=trips[i,6]
            newtrips[i,7]=driver_code
            #for report 2,3,4
            income_array[payment_time]+=trip_payment[i]
            m=np.where(trips[i,1]==golden_pass[:,0])
            golden_pass[m,1]+=int(trip_time[i])
            y=np.where(newtrips[i,7]==golden_driver[:,0])
            golden_driver[y,1]+=int(Z[i])
            #print(golden_pass)
            #print(drivers)
            #print(newtrips)
        else:
            newtrips[i,7]=0



def report(Input):
    
    while(Input!=0):
        if Input==1:
            #report1
            usertime=int(input('please enter a time between 1 to 150 \n'))
            x=np.where(trips[:,2]==usertime)
            #print(x)
            print('the trips done in this specific time are : \n',trips[x,:])
        elif Input==2:
            usertime=int(input('please enter a time between 1 to 150 \n'))
            #report2
            #print(income_array)
            cum_income=income_array[0:usertime+1].cumsum()
            print('the cumulative payment up till this time is : \n ',cum_income[usertime])
        elif Input==3:
            #report3
            #print(golden_pass)
            GPindex=np.argmax(golden_pass[:,1])
            print('the passenger with most trips time is :',golden_pass[GPindex,0])
        elif Input==4:
            #report4
            #print(golden_driver)
            GDindex=np.argmax(golden_driver[:,1])
            print('the busiest driver is : ', golden_driver[GDindex,0])
        elif Input==5:
            #report5
            Most_expensive=np.argmax(trip_payment)
            print('the payment of the most expensive trips is : ' ,Most_expensive)
            print('trip_code is :' , trips[Most_expensive,0],'\n',' time needed for this trip is :',trip_time[Most_expensive])
        elif Input==6:
            #report6
            #print(newtrips)
            done_demand=np.count_nonzero(newtrips[:,7])
            lost_demand=req_num-done_demand
            lost_perc=(lost_demand/100)*100
            print('percentage of lost demands is :',lost_perc)
        elif Input==7:
            #report 7
            print(whole)
            A=trips[np.logical_and(np.logical_and(trips[:,4]<50,trips[:,4]>0),np.logical_and(trips[:,3]<50,trips[:,3]>0))]
            A_perc=((np.shape(A)[0])/req_num)*100
            C=trips[np.logical_and(np.logical_and(trips[:,4]<=100,trips[:,4]>=50),np.logical_and(trips[:,3]<=100,trips[:,3]>=50))]
            C_perc=((np.shape(C)[0])/req_num)*100
            D=trips[np.logical_and(np.logical_and(trips[:,3]<50,trips[:,3]>0),np.logical_and(trips[:,4]<=100,trips[:,4]>=50))]
            D_perc=((np.shape(D)[0])/req_num)*100
            B=trips[np.logical_and(np.logical_and(trips[:,3]<=100,trips[:,3]>=50),np.logical_and(trips[:,4]<50,trips[:,4]>0))]
            B_perc=((np.shape(B)[0])/req_num)*100
            #print(B,D,C,A)
            print('the percentage of requests of B area is :',B_perc)
            print('the percentage of requests of D area is :',D_perc)
            print('the percentage of requests of C area is :',C_perc)
            print('the percentage of requests of A area is :',A_perc)
        elif Input==8:
            #report 8
            A_C=trips[np.logical_and(np.logical_and(np.logical_and(trips[:,4]<50,trips[:,4]>0),np.logical_and(trips[:,3]<50,trips[:,3]>0)),
                                     np.logical_and(np.logical_and(trips[:,6]<=100,trips[:,6]>=50),np.logical_and(trips[:,5]<=100,trips[:,5]>=50)))]
            #print(A_C)
            last_one=np.unique(A_C[:,1],False,False,True)
            print(last_one)
            MAX=np.argwhere(last_one[1]==np.amax(last_one[1]))
            print('passengers with the most request from A to C are: \n ',last_one[0][MAX])
        elif Input!=(1,2,3,4,5,6,7,8):
            print('please enter only one of the option given above! \n')
            
        Input=int(input('Which option do you want to see? enter the optional Number : \n'))   
    else:
       exit()









disttype=int(input('please enter "1" if you choose Elucilidean and press "0" if you want Manhattan\n'))
while (disttype!=0 and disttype!=1 ):
    print('please enter either "0" or "1" .')
    disttype=int(input('please enter "1" if you choose Elucilidean and press "0" if you want Manhattan\n'))
print(' number 1 for report of a specific time and its trips. \n')
print('numper 2 for report of the cumulative income up until a specific time. \n')
print('number 3 for report of the Golden Passenger(with most trip times. \n')
print('number 4 for report of the GOlden driver (with most distance. \n')
print('number 5 for report of the most expensive trip.\n')
print('number 6 for report of the percentage of lost demand to all demands. \n')
print('number 7 for report of the percentage of demand in each 4 areas. \n')
print('number 8 for report of the passenger with most trips starting in "A" and ending in "C". \n')
print('for exiting the program, enter "0" \n.')
Input=int(input('Which option do you want to see? enter the optional Number : \n'))    


income_array=np.random.randint(0,1,200)
#print(trips)
mycount1=np.count_nonzero(users[users[:,0]<2999][:,0])
#print(mycount1)
mycount2=np.count_nonzero(users[users[:,0]>2999][:,0])
#print(mycount2)
golden_pass=np.column_stack((np.arange(3001,3001+mycount2),np.random.randint(0,1,mycount2)))
golden_driver=np.column_stack((np.arange(1001,1001+mycount1),np.random.randint(0,1,mycount1)))
newarray=np.arange(0,1,mycount1)

#for report 7 and 8:
a=np.full((50,50),'A')
b=np.full((50,50),'B')
c=np.full((50,50),'C')
d=np.full((50,50),'D')
whole_right=np.vstack((a,d))
whole_left=np.vstack((b,c))
whole=np.hstack((whole_left,whole_right))

#for all
x2=trips[:,5]
x1=trips[:,3]
y2=trips[:,6]
y1=trips[:,4]
t=trips[:,2]
distance(disttype,x1,x2,y1,y2)
duration(Z)
payment(trip_time)
alloc(disttype)
report(Input)
#print(newtrips)
#print(drivers)
