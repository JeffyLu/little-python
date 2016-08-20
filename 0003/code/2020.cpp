#include<stdio.h>
#include<math.h>

//acm
//hdu2020
int main()
{
	int n,i,j,t,x,y;
	int a[100];
	while(scanf("%d",&n),n)
	{
		for(i=0;i<n;i++)
			scanf("%d",&a[i]);
		for(j=0;j<n-1;j++)
			for(i=0;i<n-1-j;i++)
			{
				x=abs(a[i]);y=abs(a[i+1]);
				if(x<y)
				{t=a[i];a[i]=a[i+1];a[i+1]=t;}
			}
		for(i=0;i<n;i++)
			printf(i==0?"%d":" %d",a[i]);
		printf("\n");
	}
	return 0;
}