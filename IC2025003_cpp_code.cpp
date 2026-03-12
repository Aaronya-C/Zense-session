#include<bits/stdc++.h>
using namespace std;
int main()
{
    vector<int> a={3,4,78,100,121,256};
    int target=4,ans=-1;
    int r=6,l=0;
    while(l<=r)
    {
        int mid = (l+r)/2;
        if(a[mid]== target)
        {
            ans=mid;
            break;
        }
        else if(a[mid]<target)
        {
            l=mid+1;
        }
        else
        {
            r=mid-1;
        }
    }
    //ans contains the answer
}