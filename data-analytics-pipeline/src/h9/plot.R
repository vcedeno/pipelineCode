#! /usr/bin/Rscript
require(ggplot2)
library(ggplot2)


#Read data
args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) 
{
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} 
print(args[1])
data<-read.csv(args[1],header=TRUE)
data<-read.csv('/Users/vcedeno/Desktop/dataAnalytics/data-analytics-pipeline/test/results/h9/output/all/tsData.csv',header=TRUE)

data$fracRequestSent <- data$repliesReceived/data$requestsSent
data$fracRequestSent[is.nan(data$fracRequestSent)] <- 0

dir=paste(getwd(),"data-analytics-pipeline/test/results/h9/output/all",sep = "/")

fnamepar=paste(dir,'plot.pdf',sep = "/")

wsize=12
hsize=12
plot=ggplot(data,aes(x=fracRequestSent,y=requestsSent,color=as.factor(category),shape=type)) +
  geom_point(size=5) +scale_shape_manual(values=seq(0,8))

ggsave(fnamepar,plot=plot,width = wsize, height = hsize)
