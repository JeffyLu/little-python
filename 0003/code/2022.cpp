#include<stdio.h>
#include<math.h>

//Ö÷º¯Êý
int main()
{
	int m,n,i,j,h,l;
	double x,t;
	/*
	   whileÑ­»·
	*/
	while(scanf("%d%d",&m,&n)!=EOF)
	{
		t=h=l=0;
		for(i=0;i<m;i++)
			for(j=0;j<n;j++)
			{
				scanf("%lf",&x);
				if(fabs(x)>fabs(t))
				{
					t=x;
					h=i;
					l=j;
				}
			}
		printf("%d %d %.0lf\n",h+1,l+1,t);
	}
	return 0;
}	