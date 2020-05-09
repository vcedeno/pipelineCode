#! /usr/bin/Rscript
require(foreign)
require(nnet)
library(foreign)
library(VGAM)

#Read data
args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) 
{
  stop("At least four argument must be supplied (input file).n", call.=FALSE)
} 


TS_k2<-read.csv(args[1],header=TRUE)
TS_k4<-read.csv(args[2],header=TRUE)
TS_k6<-read.csv(args[3],header=TRUE)
TS_k8<-read.csv(args[4],header=TRUE)

dir=paste(getwd(),"property-inference-pipeline/test/results/h2/dynamic_word/",sep = "/")
dirpro=paste(getwd(),"modeling-and-simulation-pipeline/json-schema/h1/input/datasets/dynamic_word/",sep = "/")

#k=2
#Read data
TS<-TS_k2
TS[1:5,1:10]
n<-length(TS[,1]) #15
m<-length(TS[1,])-3 #300
k<-2


#rearrange data
x<-NULL
num.x<-NULL
for (ii in 1:4){
  for (jj in 1:4){
    count<-0
    for (i in 1:(n/5)*5-4){
      for (j in 1:(m-1)+3){
        if (TS[i,j]==ii & TS[i,(j+1)]==jj){
          x<-rbind(x,c(ii,jj,TS[(i+1:4),j]))
          count<-count+1
        }
      }
    }
    num.x<-c(num.x,count)
  }
}  
dim(x)

# ncount summarize the number of data for 16 transitions.
ncount<-data.frame(matrix(num.x,nrow=4))
colnames(ncount)<-c('initial 1','initial 2','initial 3','initial 4')
rownames(ncount)<-c('final 1','final 2','final 3','final 4')
ncount<-t(ncount)
datasum<-data.frame(matrix(c(rep(NA,16)),nrow=4))
for (i in 1:4){
  datasum[i,]<-ncount[i,]/sum(ncount[i,])
}
rownames(datasum)<-c('initial 1','initial 2','initial 3','initial 4')
colnames(datasum)<-c('final 1','final 2','final 3','final 4')
ncount_k2<-ncount;datasum_k2<-datasum

data<-data.frame(x)

#
add<-NULL
for (i in 3:6){
  add<-cbind(add,data[,i]*(k-5)/sqrt(20))
}
for (i in 3:6){
  add<-cbind(add,data[,i]*(((k-5)/2)^2-15/12)/2)
}
data<-cbind(data,add)


#first column is the initial state (at t second)
#second column is the final state (at t+1 second)
#3-6 column is four x variables ('buffer','letter','word','constant').
colnames(data)<-c('initial','final','buffer','letter','word','constant',
                  'buffer_k','letter_k','word_k','constant_k',
                  'buffer_k2','letter_k2','word_k2','constant_k2')
data$k<-2
data_k2<-data
data1_k2<-data[which(data$initial==1),-1] #data1=intial state is 1
data2_k2<-data[which(data$initial==2),-1] #data2=intial state is 2
data3_k2<-data[which(data$initial==3),-1] #data3=intial state is 3
data4_k2<-data[which(data$initial==4),-1] #data4=intial state is 4
dim(data1_k2);dim(data2_k2);dim(data3_k2);dim(data4_k2)

#k=4
#Read data
TS<-TS_k4
TS[1:5,1:10]
n<-length(TS[,1]) #405
m<-length(TS[1,])-3 #300
k<-4


#rearrange data
x<-NULL
num.x<-NULL
for (ii in 1:4){
  for (jj in 1:4){
    count<-0
    for (i in 1:(n/5)*5-4){
      for (j in 1:(m-1)+3){
        if (TS[i,j]==ii & TS[i,(j+1)]==jj){
          x<-rbind(x,c(ii,jj,TS[(i+1:4),j]))
          count<-count+1
        }
      }
    }
    num.x<-c(num.x,count)
  }
}  
dim(x)

# ncount summarize the number of data for 16 transitions.
ncount<-data.frame(matrix(num.x,nrow=4))
colnames(ncount)<-c('initial 1','initial 2','initial 3','initial 4')
rownames(ncount)<-c('final 1','final 2','final 3','final 4')
ncount<-t(ncount)
datasum<-data.frame(matrix(c(rep(NA,16)),nrow=4))
for (i in 1:4){
  datasum[i,]<-ncount[i,]/sum(ncount[i,])
}
rownames(datasum)<-c('initial 1','initial 2','initial 3','initial 4')
colnames(datasum)<-c('final 1','final 2','final 3','final 4')
ncount_k4<-ncount;datasum_k4<-datasum

data<-data.frame(x)

#
add<-NULL
for (i in 3:6){
  add<-cbind(add,data[,i]*(k-5)/sqrt(20))
}
for (i in 3:6){
  add<-cbind(add,data[,i]*(((k-5)/2)^2-15/12)/2)
}
data<-cbind(data,add)


#first column is the initial state (at t second)
#second column is the final state (at t+1 second)
#3-6 column is four x variables ('buffer','letter','word','constant').
colnames(data)<-c('initial','final','buffer','letter','word','constant',
                  'buffer_k','letter_k','word_k','constant_k',
                  'buffer_k2','letter_k2','word_k2','constant_k2')
data$k<-4
data_k4<-data
data1_k4<-data[which(data$initial==1),-1] #data1=intial state is 1
data2_k4<-data[which(data$initial==2),-1] #data2=intial state is 2
data3_k4<-data[which(data$initial==3),-1] #data3=intial state is 3
data4_k4<-data[which(data$initial==4),-1] #data4=intial state is 4
dim(data1_k4);dim(data2_k4);dim(data3_k4);dim(data4_k4)


#k=6
#Read data
TS<-TS_k6
TS[1:5,1:10]
n<-length(TS[,1]) #105
m<-length(TS[1,])-3 #300
k<-6


#rearrange data
x<-NULL
num.x<-NULL
for (ii in 1:4){
  for (jj in 1:4){
    count<-0
    for (i in 1:(n/5)*5-4){
      for (j in 1:(m-1)+3){
        if (TS[i,j]==ii & TS[i,(j+1)]==jj){
          x<-rbind(x,c(ii,jj,TS[(i+1:4),j]))
          count<-count+1
        }
      }
    }
    num.x<-c(num.x,count)
  }
}  
dim(x)

# ncount summarize the number of data for 16 transitions.
ncount<-data.frame(matrix(num.x,nrow=4))
colnames(ncount)<-c('initial 1','initial 2','initial 3','initial 4')
rownames(ncount)<-c('final 1','final 2','final 3','final 4')
ncount<-t(ncount)
datasum<-data.frame(matrix(c(rep(NA,16)),nrow=4))
for (i in 1:4){
  datasum[i,]<-ncount[i,]/sum(ncount[i,])
}
rownames(datasum)<-c('initial 1','initial 2','initial 3','initial 4')
colnames(datasum)<-c('final 1','final 2','final 3','final 4')
ncount_k6<-ncount;datasum_k6<-datasum

data<-data.frame(x)

#
add<-NULL
for (i in 3:6){
  add<-cbind(add,data[,i]*(k-5)/sqrt(20))
}
for (i in 3:6){
  add<-cbind(add,data[,i]*(((k-5)/2)^2-15/12)/2)
}
data<-cbind(data,add)


#first column is the initial state (at t second)
#second column is the final state (at t+1 second)
#3-6 column is four x variables ('buffer','letter','word','constant').
colnames(data)<-c('initial','final','buffer','letter','word','constant',
                  'buffer_k','letter_k','word_k','constant_k',
                  'buffer_k2','letter_k2','word_k2','constant_k2')
data$k<-6
data_k6<-data
data1_k6<-data[which(data$initial==1),-1] #data1=intial state is 1
data2_k6<-data[which(data$initial==2),-1] #data2=intial state is 2
data3_k6<-data[which(data$initial==3),-1] #data3=intial state is 3
data4_k6<-data[which(data$initial==4),-1] #data4=intial state is 4
dim(data1_k6);dim(data2_k6);dim(data3_k6);dim(data4_k6)


#k=8
#Read data
TS<-TS_k8
TS[1:5,1:10]
n<-length(TS[,1]) #210
m<-length(TS[1,])-3 #300
k<-8


#rearrange data
x<-NULL
num.x<-NULL
for (ii in 1:4){
  for (jj in 1:4){
    count<-0
    for (i in 1:(n/5)*5-4){
      for (j in 1:(m-1)+3){
        if (TS[i,j]==ii & TS[i,(j+1)]==jj){
          x<-rbind(x,c(ii,jj,TS[(i+1:4),j]))
          count<-count+1
        }
      }
    }
    num.x<-c(num.x,count)
  }
}  
dim(x)

# ncount summarize the number of data for 16 transitions.
ncount<-data.frame(matrix(num.x,nrow=4))
colnames(ncount)<-c('initial 1','initial 2','initial 3','initial 4')
rownames(ncount)<-c('final 1','final 2','final 3','final 4')
ncount<-t(ncount)
datasum<-data.frame(matrix(c(rep(NA,16)),nrow=4))
for (i in 1:4){
  datasum[i,]<-ncount[i,]/sum(ncount[i,])
}
rownames(datasum)<-c('initial 1','initial 2','initial 3','initial 4')
colnames(datasum)<-c('final 1','final 2','final 3','final 4')
ncount_k8<-ncount;datasum_k8<-datasum

data<-data.frame(x)
data$buffer
data$letter
data$word
data$constant
summary(data$buffer) #1,3,5
summary(data$letter) #3,6,9
summary(data$word)#1,5,9
summary(data$constant)#0,20,40

#
add<-NULL
for (i in 3:6){
  add<-cbind(add,data[,i]*(k-5)/sqrt(20))
}
for (i in 3:6){
  add<-cbind(add,data[,i]*(((k-5)/2)^2-15/12)/2)
}
data<-cbind(data,add)


#first column is the initial state (at t second)
#second column is the final state (at t+1 second)
#3-6 column is four x variables ('buffer','letter','word','constant').
colnames(data)<-c('initial','final','buffer','letter','word','constant',
                  'buffer_k','letter_k','word_k','constant_k',
                  'buffer_k2','letter_k2','word_k2','constant_k2')
data$k<-8
data_k8<-data
data1_k8<-data[which(data$initial==1),-1] #data1=intial state is 1
data2_k8<-data[which(data$initial==2),-1] #data2=intial state is 2
data3_k8<-data[which(data$initial==3),-1] #data3=intial state is 3
data4_k8<-data[which(data$initial==4),-1] #data4=intial state is 4
dim(data1_k8);dim(data2_k8);dim(data3_k8);dim(data4_k8)


#
data1<-rbind(data1_k2,data1_k4,data1_k6,data1_k8)
data2<-rbind(data2_k2,data2_k4,data2_k6,data2_k8)
data3<-rbind(data3_k2,data3_k4,data3_k6,data3_k8)
data4<-rbind(data4_k2,data4_k4,data4_k6,data4_k8)

#multinomial logistic regression
#v_k2<-c(1,(k-5)/sqrt(20),(((k-5)/2)^2-15/12)/2);v_k4<-c(1,4,4^2);v_k6<-c(1,6,6^2);v_k8<-c(1,8,8^2)
v<-NULL
for (i in 1:8){
  v<-cbind(v,c(1,(i-5)/sqrt(20),(((i-5)/2)^2-15/12)/2))
}
v_k2<-v[,2];v_k4<-v[,4];v_k6<-v[,6];v_k8<-v[,8]

mlog1<-multinom(final~.,family=multinomial,data=data1[,-14])
summary(mlog1)
sum1<-summary(mlog1)
betam.e1<-coef(mlog1)

A12<-rbind(c(betam.e1[1,1],0,0),matrix(betam.e1[1,-1],ncol=3,byrow=FALSE))
A13<-rbind(c(betam.e1[2,1],0,0),matrix(betam.e1[2,-1],ncol=3,byrow=FALSE))
A14<-rbind(c(betam.e1[3,1],0,0),matrix(betam.e1[3,-1],ncol=3,byrow=FALSE))

B12<-A12%*%v_k4


mlog2<-multinom(final~.,family=multinomial,data=data2[,-14])
summary(mlog2)
betam.e2<-coef(mlog2)
A22<-rbind(c(betam.e2[1,1],0,0),matrix(betam.e2[1,-1],ncol=3,byrow=FALSE))
A24<-rbind(c(betam.e2[2,1],0,0),matrix(betam.e2[2,-1],ncol=3,byrow=FALSE))





mlog3<-multinom(final~.,family=multinomial,data=data3[,-14])
summary(mlog3)
betam.e3<-coef(mlog3)
A32<-rbind(c(betam.e3[1,1],0,0),matrix(betam.e3[1,-1],ncol=3,byrow=FALSE))
A33<-rbind(c(betam.e3[2,1],0,0),matrix(betam.e3[2,-1],ncol=3,byrow=FALSE))



mlog4<-multinom(final~.,family=multinomial,data=data4[,-14])
summary(mlog4)
betam.e4<-coef(mlog4)
A42<-rbind(c(betam.e4[1,1],0,0),matrix(betam.e4[1,-1],ncol=3,byrow=FALSE))
A43<-rbind(c(betam.e4[2,1],0,0),matrix(betam.e4[2,-1],ncol=3,byrow=FALSE))
A44<-rbind(c(betam.e4[3,1],0,0),matrix(betam.e4[3,-1],ncol=3,byrow=FALSE))


#
ncount<-ncount_k2+ncount_k4+ncount_k6+ncount_k8
datasum<-NULL
for (i in 1:4){
  datasum<-rbind(datasum,ncount[i,]/sum(ncount[i,]))
}


#
B1<-NULL;B2<-NULL;B3<-NULL;B4<-NULL
#for (k in 1:8){
  #B1[[k]]<-t(cbind(A12%*%v[,k],A13%*%v[,k],A14%*%v[,k]))
  #B2[[k]]<-t(cbind(A22%*%v[,k],A24%*%v[,k]))
  #B3[[k]]<-t(cbind(A32%*%v[,k],A33%*%v[,k]))
  #B4[[k]]<-t(cbind(A42%*%v[,k],A43%*%v[,k],A44%*%v[,k]))
#}
#for (k in 1:8){
#  print(k)
#  print(B1[[k]]);print(B2[[k]]);print(B3[[k]]);print(B4[[k]])
#}

for (k in 1:8){
  B1[[k]]<-t(cbind(c(rep(0,5)),A12%*%v[,k],A13%*%v[,k],A14%*%v[,k]))
  B2[[k]]<-t(cbind(c(rep(0,5)),A22%*%v[,k],c(-Inf,0,0,0,0),A24%*%v[,k]))
  B3[[k]]<-t(cbind(c(rep(0,5)),A32%*%v[,k],A33%*%v[,k],c(-Inf,0,0,0,0)))
  B4[[k]]<-t(cbind(c(rep(0,5)),A42%*%v[,k],A43%*%v[,k],A44%*%v[,k]))
}

B<-NULL
for (k in 1:8){
  B[[k]]<-rbind(B1[[k]],B2[[k]],B3[[k]],B4[[k]])
}

dir2=paste(dir,"hierarchy_k=",sep = "")
dir22=paste(dirpro,"hierarchy_k=",sep = "")
for (k in 1:8){
  filename2=paste(dir2,k,sep = "")
  filename22=paste(dir22,k,sep = "")
  filename=paste(filename2,".txt",sep = "")
  filenamepro=paste(filename22,".txt",sep = "")
  write.table(B[[k]],row.names=FALSE,col.names=FALSE,filename)
  write.table(B[[k]],row.names=FALSE,col.names=FALSE,filenamepro)
}


A<-NULL
A[[1]]<-rbind(A12,A13,A14)
A[[2]]<-rbind(A22,A24)
A[[3]]<-rbind(A32,A33)
A[[4]]<-rbind(A42,A43,A44)

dir2=paste(dir,"A_matrix_initial_k=",sep = "")
dir22=paste(dirpro,"A_matrix_initial_k=",sep = "")
for (k in 1:4){
  filename2=paste(dir2,k,sep = "")
  filename22=paste(dir22,k,sep = "")
  filename=paste(filename2,".txt",sep = "")
  filenamepro=paste(filename22,".txt",sep = "")
  write.table(A[[k]],row.names=FALSE,col.names=FALSE,filename)
  write.table(A[[k]],row.names=FALSE,col.names=FALSE,filenamepro)
}

#for (k in 1:4){
#  filename2=paste(dir2,k,sep = "")
#  filename=paste(filename2,".txt",sep = "")
#  write.csv(A[[k]],filename)
#}

A_00<-rep(0,5)
A_NE<-c(c(-Inf,0,0,0,0))
AA<-NULL
AA[[1]]<-rbind(A_00,A12[,1],A13[,1],A14[,1],
          A_00,A22[,1],A_NE,A24[,1],
          A_00,A32[,1],A33[,1],A_NE,
          A_00,A42[,1],A43[,1],A44[,1])

AA[[2]]<-rbind(A_00,A12[,2],A13[,2],A14[,2],
          A_00,A22[,2],A_00,A24[,2],
          A_00,A32[,2],A33[,2],A_00,
          A_00,A42[,2],A43[,2],A44[,2])

AA[[3]]<-rbind(A_00,A12[,3],A13[,3],A14[,3],
          A_00,A22[,3],A_00,A24[,3],
          A_00,A32[,3],A33[,3],A_00,
          A_00,A42[,3],A43[,3],A44[,3])


B_test<-AA[[1]]*v_k2[1]+AA[[2]]*v_k2[2]+AA[[3]]*v_k2[3]
B_test[is.na(B_test[,])]<--Inf

dir2=paste(dir,"A_matrix_k=",sep = "")
dir22=paste(dirpro,"A_matrix_k=",sep = "")
for (k in 0:2){
  rownames(AA[[k+1]])<-NULL
  filename2=paste(dir2,k,sep="")
  filename22=paste(dir22,k,sep="")
  filename=paste(filename2,'.txt',sep="")
  filenamepro=paste(filename22,'.txt',sep="")
  write.table(AA[[k+1]],row.names=FALSE,col.names=FALSE,filename)
  write.table(AA[[k+1]],row.names=FALSE,col.names=FALSE,filenamepro)
}

