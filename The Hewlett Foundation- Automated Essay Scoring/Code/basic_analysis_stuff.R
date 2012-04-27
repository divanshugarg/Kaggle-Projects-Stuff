library(ggplot2)

length_score <- read.csv("/Users/sinn/Documents/Kaggle/The Hewlett Foundation- Automated Essay Scoring/set08_count_score.txt", header=FALSE, stringsAsFactors=FALSE, sep = '\t')

plot(length_score$V1, length_score$V5)
summary(length_score$V5)

ggplot(length_score, aes(x=V5))+geom_histogram()
ggplot(length_score, aes(x=V1, y=V5)) + 
		geom_point() +
		geom_smooth(method = 'lm')		# lin fit is pretty horrible
		
type_len_score <- read.csv('/Users/sinn/Documents/Kaggle/The Hewlett Foundation- Automated Essay Scoring/type_len_score_data.txt', stringsAsFactors=FALSE, header=FALSE, sep='\t')
not_8 <- subset(type_len_score, V1<8)
not_7 <- subset(not_8, V1<7)
not_1 <- subset(not_7, V1>1)
ggplot(not_1, aes(x=V2, y=V6, color=V1)) + geom_point()
ggplot(not_1, aes(x=V6)) + geom_histogram()