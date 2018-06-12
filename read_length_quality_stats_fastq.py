#!/usr/local/bin/python
# Khushbu Patel | 05/29/2018
#|__This script requires Python 3.4 and modules - numpy & scipy
#|__extracts the quality string and determine the length and average quality score of each read
#|__Converts the raw values for each read set into descriptive statistics
#|__Provides descriptive stats for Read Lengths and Read Qualities, number and percentage of reads below Q30 and Ambiguous base counts
# Usage: ./extract_quality_and_stats_fastq.py [Read_1.fastq] [Read_2.fastq]

import numpy as np
import sys
from scipy.stats import skew,mstats


# ------------------------------------------ DECLARATIONS AND INITIALIZATIONS ------------------------------------------------#
quality_scores_R1 = []
quality_scores_R2 = []
average_quality = 0
read1_length = []
read2_length = []
inserts = []
insert_sizes = []
R1_le_249 = 0
R1_gt_249 = 0
R1_le_149 = 0
R1_gt_149 = 0
R1_le_299 = 0
R1_gt_299 = 0
R2_le_249 = 0
R2_gt_249 = 0
R2_le_149 = 0
R2_gt_149 = 0
R2_le_299 = 0
R2_gt_299 = 0
countN1 = 0
countN2 = 0
Q1_lt_30 = 0
Q2_lt_30 = 0

# ------------------------------------------ FUNCTIONS ------------------------------------------------#
# To parse fastq file
def parseFastq(fastq_infile):
	sequences = []
	qualities = []
	
	with open(fastq_infile,"r", encoding="utf8", errors='ignore') as f:
		while True:	
			f.readline()
			seq = f.readline().rstrip()		# gets sequence line
			f.readline()
			qual = f.readline().rstrip()	# gets quality line
			if len(seq) == 0:		# if seq length is 0; reached end of file so break out of the loop
				break	
			sequences.append(seq)	# append seq to sequences list
			qualities.append(qual)	# append qual to sequences list
	
	return sequences,qualities
	


# To convert ASCII  to quality scores
def phred33toQ(qual):
	return ord(qual) - 33	# ord converts char to ASCII values and returns
	


# To calculate descriptive stats
def stats(in_array):
	a = np.array(in_array)
	mean = a.mean()
	std_dev = a.std()
	variance = np.var(a)
	Q1 = np.percentile(a,25)
	median = np.percentile(a,50)
	Q3 = np.percentile(a,75)
	skewness = skew(a)
	geometric_mean = mstats.gmean(a)
	
	high = []
	low = []
	IQR = Q3 - Q1
	lower = Q1 - (1.5*IQR)
	upper = Q3 - (1.5*IQR)
	
	if(min(in_array) < lower):
		low_whisker = min(in_array)
	else:
		low_whisker = min(in_array)
	
	if(max(in_array) > upper):
		high_whisker = max(in_array)
	else:
		high_whisker = max(in_array)
	
	return mean,std_dev,variance,Q1,median,Q3,skewness,geometric_mean,low_whisker,high_whisker
	
	
	
# Ambiguous base counts
def countN(seq):
	count = 0
	for s in seq:
		count += s.count("N")
	return count

	
# quality thresholds
def Q30(qual_list):
	count_lt_30 = 0
	for x in qual_list:
		if(x < 30):
			count_lt_30 += 1
		else:
			continue
	return count_lt_30
	
	
# To get average quality scores for each read1 
def qual_score(qual):
	quality_scores = []
	read_len = []
	for Q in qual:
		score = 0
		read_len.append(len(Q))
		for val in Q:
			score += phred33toQ(val)
		average_quality = (score/len(Q))	
		quality_scores.append(average_quality)	
	return read_len,quality_scores
	

# read Length thresholds 
def threshold(lengths):
	len_le_149 = 0
	len_gt_149 = 0
	len_le_249 = 0
	len_gt_249 = 0
	len_le_299 = 0
	len_gt_299 = 0
	for x in lengths:
		if(x <= 149):
			len_le_149 += 1
		elif(x > 149):
			len_gt_149 += 1
		elif(x <= 249):
			len_le_249 += 1
		elif(x > 249):
			len_gt_249 += 1
		elif(x <= 299):
			len_le_299 += 1
		elif(x > 299):
			len_gt_299 += 1

	return len_le_149,len_gt_149,len_le_249,len_gt_249,len_le_299,len_gt_299
	
	
def Print_read_length(mean,stdDev,var,Q1,median,Q3,skew,gmean,lwhisker,hwhisker,len_le_149,len_gt_149,len_le_249,len_gt_249,len_le_299,len_gt_299):
	print("Normal Mean = %5.5f" % mean)
	print("Geometric mean = %5.5f" % gmean)
	print("standard deviation = %5.5f" % stdDev)
	print("Variance = %5.5f" % var)
	print("1st quartile = %5.5f" % Q1)
	print("Median = %5.5f" % median)
	print("3rd quartile = %5.5f" % Q3)
	print("Skewness = %5.5f" % skew)
	print("Lower whisker = %5.5f" % lwhisker)
	print("upper whisker = %5.5f" % hwhisker)
	print("Reads > 149 = %d" % len_gt_149)
	print("Reads <= 149 = %d" % len_le_149)
	print("Reads > 249 = %d" % len_gt_249)
	print("Reads <= 249 = %d" % len_le_249)
	print("Reads > 299 = %d" % len_gt_299)
	print("Reads <= 299 = %d" % len_le_299)
	
	
def Print_read_qual(mean,stdDev,var,Q1,median,Q3,skew,gmean,lwhisker,hwhisker,qual_lt_30,perc_qual_lt_30,count_ambi):
	print("Normal Mean = %5.5f" % mean)
	print("Geometric mean = %5.5f" % gmean)
	print("standard deviation = %5.5f" % stdDev)
	print("Variance = %5.5f" % var)
	print("1st quartile = %5.5f" % Q1)
	print("Median = %5.5f" % median)
	print("3rd quartile = %5.5f" % Q3)
	print("Skewness = %5.5f" % skew)
	print("Lower whisker = %5.5f" % lwhisker)
	print("upper whisker = %5.5f" % hwhisker)
	print("Reads with quality less than 30 = %d" % qual_lt_30)
	print("Percentage of Reads with quality less than 30 = %5.5f" % perc_qual_lt_30)
	print("Ambiguous base counts = %d" % count_ambi)
	
	
# ---------------------------------------------------- MAIN ----------------------------------------------------------------- #	

# command line arguments
fastq1 = sys.argv[1]
fastq2 = sys.argv[2]

# function call
seqs1,quals1 = parseFastq(fastq1)	# takes in fastq file as an input from command line and passes it as an argument to parseFastq function. Returns sequences and qualities and stores in seqs & quals
seqs2,quals2 = parseFastq(fastq2)


	
print("Number of reads for R1_file is %d"  % len(seqs1))
print("Number of reads for R2_file is %d"  % len(seqs2))		


# read Length thresholds 
R1_le_149,R1_gt_149,R1_le_249,R1_gt_249,R1_le_299,R1_gt_299 = threshold(read1_length)
R2_le_149,R2_gt_149,R2_le_249,R2_gt_249,R2_le_299,R2_gt_299 = threshold(read2_length)


# average quality scores for each read
read1_length,quality_scores_R1 = qual_score(quals1)
read2_length,quality_scores_R2 = qual_score(quals2)

# quality threshold function call
Q1_lt_30 = Q30(quality_scores_R1)
Q2_lt_30 = Q30(quality_scores_R2)

percent_reads_lt_30_R1 = Q1_lt_30/len(seqs1) * 100
percent_reads_lt_30_R2 = Q2_lt_30/len(seqs2) * 100

# Ambiguous base function call
countN1 = countN(seqs1)
countN2 = countN(seqs2)

# Descriptive stats for read1 length
r_mean,r_stdDev,r_var,r_Q1,r_median,r_Q3,r_skew,r_gmean,r_lwhisker,r_hwhisker = stats(read1_length)
# Descriptive stats for read2 length
i_mean,i_stdDev,i_var,i_Q1,i_median,i_Q3,i_skew,i_gmean,i_lwhisker,i_hwhisker = stats(read2_length)


# Descriptive stats for Q1 quality
q_mean,q_stdDev,q_var,q_Q1,q_median,q_Q3,q_skew,q_gmean,q_lwhisker,q_hwhisker = stats(quality_scores_R1)
# Descriptive stats for Q2 quality
s_mean,s_stdDev,s_var,s_Q1,s_median,s_Q3,s_skew,s_gmean,s_lwhisker,s_hwhisker = stats(quality_scores_R2)


# calling Print function
print("------ Descriptive stats for R1 Lengths----------")
Print_read_length(r_mean,r_stdDev,r_var,r_Q1,r_median,r_Q3,r_skew,r_gmean,r_lwhisker,r_hwhisker,R1_le_149,R1_gt_149,R1_le_249,R1_gt_249,R1_le_299,R1_gt_299) # R1 stats
print("------ Descriptive stats for R2 Lengths----------")
Print_read_length(i_mean,i_stdDev,i_var,i_Q1,i_median,i_Q3,i_skew,i_gmean,i_lwhisker,i_hwhisker,R2_le_149,R2_gt_149,R2_le_249,R2_gt_249,R2_le_299,R2_gt_299) # R2 stats
print("------ Descriptive stats for R1 Quality----------")
Print_read_qual(q_mean,q_stdDev,q_var,q_Q1,q_median,q_Q3,q_skew,q_gmean,q_lwhisker,q_hwhisker,Q1_lt_30,percent_reads_lt_30_R1,countN1)	# Q1 stats
print("------ Descriptive stats for R2 Quality----------")
Print_read_qual(s_mean,s_stdDev,s_var,s_Q1,s_median,s_Q3,s_skew,s_gmean,s_lwhisker,s_hwhisker,Q2_lt_30,percent_reads_lt_30_R2,countN2)	# Q2 stats
