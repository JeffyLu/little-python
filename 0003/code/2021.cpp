#include<stdio.h>

/*
acm
hdu
2021
*/
int main()
{
	int n,i,s,x;
	while(scanf("%d",&n),n)
	{
		s=0;
		for(i=0;i<n;i++)
		{
			scanf("%d",&x);
			s=s+x/100;
			x=x%100;
			s=s+x/50;
			x=x%50;
			s=s+x/10;
			x=x%10;
			s=s+x/5;
			x=x%5;
			s=s+x/2;
			x=x%2;
			s=s+x/1;
		}
		printf("%d\n",s);
	}
	return 0;
}
