import pymongo
import facebook
from math import sqrt

#conn=pymongo.Connection('localhost',27017)
#db=conn.likes

ACCESS_TOKEN=''

g=facebook.GraphAPI(ACCESS_TOKEN)
friends = g.get_connections("me", "friends")['data']
def count_cats(likes_list=[]):
    cat_dict={}
    for item in likes_list:
        assert isinstance(item,dict)
        if item.has_key('category'):
            cat=item['category']
            cat_dict[cat]=cat_dict.get(cat,0)+1
    return cat_dict

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(like_cats,p1,p2):
# Get the list of mutually liked categories
	si={}
	for item in like_cats[p1]:
		if item in like_cats[p2]: si[item]=1
	# Find the number of elements
	n=len(si)
	# if they are no categories in common, return 0
	if n==0: return 0
	# Add up all the preferences
	sum1=sum([like_cats[p1][it] for it in si])
	sum2=sum([like_cats[p2][it] for it in si])
	# Sum up the squares
	sum1Sq=sum([pow(like_cats[p1][it],2) for it in si])
	sum2Sq=sum([pow(like_cats[p2][it],2) for it in si])
	# Sum up the products
	pSum=sum([like_cats[p1][it]*like_cats[p2][it] for it in si])
	# Calculate Pearson score
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0: return 0
	r=num/den
	return r #-1<=r<=1 with 1 being the most similar and -1 the most dissimilar

        
likes = { friend['name'] : count_cats(g.get_connections(friend['id'], "likes")['data'])
for friend in friends[:10] } #only 10 friends to save time 

####Usage
#print sim_pearson(likes,friend1,friend2) 
