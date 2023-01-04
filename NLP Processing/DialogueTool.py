#-------------------------------------------------------------------------------------------------#
# Executed with Python 3.10 (3.11 have dependency issues with tensorflow as of writing the code)
# All required installs are ready when code is executed. 
#
# I DEEPLY apologize in advance for not making this work with notebooks, which is why I have
# tried to format the text here as nice as I possibly could. I also apologize if this is noisy.
#-------------------------------------------------------------------------------------------------#
from pip._internal import main as pipmain

### ///------------------< Optional Installations on Current Environment >------------------\\\ ###
#-------------------------------------------------------------------------------------------------#
# Feel free to comment the installation command out, should you prefer that.
#-------------------------------------------------------------------------------------------------#
pipmain(['install', 'pip'])
pipmain(['install', 'tensorflow'])
pipmain(['install', 'tensorflow-hub'])
pipmain(['install', 'numpy'])
pipmain(['install', 'matplotlib'])
pipmain(['install', 'seaborn'])
pipmain(['install', 'pandas'])

print("\n\n\n It may take a while for tensorflow to boot up for the first time \n\n\n ... \n\n\n")

### ///---------------------------------< General Imports >---------------------------------\\\ ###
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import scipy
import math
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import csv

### ///---------------------< Download and define model as embedding >----------------------\\\ ###
#-------------------------------------------------------------------------------------------------#
# Inspired use by this paper: https://arxiv.org/abs/1803.11175
# All rights to Tensorflow and Google Inc.
# All credit go to the incredibly talented people contributing to the Universal Sentence Encoder
#-------------------------------------------------------------------------------------------------#
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print ("module %s loaded" % module_url)
def embed(input):
  return model(input)

### ///----------< Define HeatMap Displaying Semtantic Textual Similiarity (STS) >----------\\\ ###
#-------------------------------------------------------------------------------------------------#
# The Heatmap displays the correlation between each value. This correlation is found as by
# calculating the angular differences between each embedded vector. This is a classification
# method suggested by the creators of Universal Sentence Encoder (USE) published by Google.p
#-------------------------------------------------------------------------------------------------#

def plot_similarity(labels, features, rotation):
  # Find the angular difference between each embedded vector
  corr = np.inner(features, features)
  sns.set(font_scale=1.2)
  g = sns.heatmap(
      corr,
      xticklabels=labels,
      yticklabels=labels,
      vmin=0,
      vmax=1,
      cmap="YlOrRd")
  g.set_xticklabels(labels, rotation=rotation)
  g.set_title("Semantic Textual Similarity")


### ///------< Define Print and Exportation for Both Python & Unreal Engine 5 (UE5) >------\\\ ###
#-------------------------------------------------------------------------------------------------#
# Prints & exports a .CSV file @ folder/subfolder of your directory. You will see the dataframe
# for UE5 is formatted differently to be read by the engine's DataTable plugin. Again, we define
# the angular difference with the vectors so we can print it out later as a dataframe.
#-------------------------------------------------------------------------------------------------#

def print_similarity(labels, lAttitude, lType, features):
  corr = np.inner(features, features)
  #print(labels)
  #print(corr)
  labelCount = len(labels)

  ### ///-----------------------< GENERAL PYTHON DATATABLE FORMAT >-----------------------\\\ ###
  #---------------------------------------------------------------------------------------------#
  # Here we simply take the original data partitions and loop our correlation value, and add
  # it as a new column so we have the individual correlation value displayed for each line.
  #---------------------------------------------------------------------------------------------#

  data = {"Label String":labels, "Attitude":lAttitude, "Type":lType}

  df = pd.DataFrame(data)
  
  for i in range(0,labelCount):
    StepCorr = (corr[i])
    
    df_new_row = pd.DataFrame({"Label Corr {}".format(i):StepCorr})
    df = pd.concat([df, df_new_row], axis=1)
    #print(StepCorr)

  os.makedirs('Output/PY', exist_ok=True)  
  df.to_csv('Output/PY/PlayerDialoguePY.csv') 

  # Print the output.
  print("Printing Python Ver DataTable ...")
  print("-------------------------------------------------------")
  print("---------< Printing Python Ver DataTable ... >---------")
  print("-------------------------------------------------------")
  print(df)

  ### ///-----------------------< UNREAL ENGINE DATATABLE FORMAT >------------------------\\\ ###
  #---------------------------------------------------------------------------------------------#
  # The procedure is the same but completely reconstructed the array so it would print out a
  # string with the appropiate format. This means numpy no longer sees it as its usual
  # functional array, but Unreal Engine's DataTable does. They need the format "()" to be read. 
  #---------------------------------------------------------------------------------------------#
  
  data2 = {"Label String":labels, "Attitude":lAttitude, "Type":lType}
  
  df2 = pd.DataFrame(data2)
  array = []

  for i in range(0,labelCount):
    corrStr = ','.join(str(x) for x in corr[i])
    start = "("
    end = ")"
    corrFormat = start + corrStr + end
    #print("Printing corrFormat {}...".format(i))
    #print(corrFormat)
    array.append(corrFormat) 

  # # Debugged to ensure the format is correct
  # print("Printing array ...")
  # print(array)

  df_new_row2 = pd.DataFrame({"Label Corrs":array})
  df2 = pd.concat([df2, df_new_row2], axis=1)

  os.makedirs('Output/UE5', exist_ok=True)  
  df2.to_csv('Output/UE5/PlayerDialogue.csv')  

  # Print the output.
  print("--------------------------------------------------------------")
  print("---------< Printing Unreal Engine Ver DataTable ... >---------")
  print("--------------------------------------------------------------")
  print(df2)

### ///-------------------------< FURTHER DATA VISUALIZATION >--------------------------\\\ ###
#---------------------------------------------------------------------------------------------#
# This is an extract of visualized data that can be plotted and can be used to investigate
# how the STS interact with the input data provided in this project. This is used in the
# report for how the STS is of further use inside of UE5. 
#
# The current visualization is a sample of each topic made from the input data, and then
# see how the STS value change and make visual threshold at topic changes or when a line
# paraphrases itself, or does not reflect the answer initiated.
#---------------------------------------------------------------------------------------------#

def plot_visualization(labels, features, rotation):
  corr = np.inner(features, features)
  labelNums = []
  labelCount = len(labels)
  for i in range(0,labelCount):
    labelNums.append(i)

  plot_x, plot_y = labelNums, corr[1]
  # print("Printing plot_x ...")
  # print(plot_x)
  # print("Printing plot_y ...")
  # print(plot_y)
  plot_x = np.reshape(plot_x, [1, labelCount]) #
  plot_y = np.reshape(plot_y, [1, labelCount]) #[-1, 1]
  plt.scatter(plot_x, plot_y, color='r', label='smartphone')

  plot_x, plot_y = labelNums, corr[9]
  plot_x = np.reshape(plot_x, [1, labelCount]) #
  plot_y = np.reshape(plot_y, [1, labelCount]) #[-1, 1]
  plt.scatter(plot_x, plot_y, color='g', label='snow')

  plot_x, plot_y = labelNums, corr[21]
  plot_x = np.reshape(plot_x, [1, labelCount]) #
  plot_y = np.reshape(plot_y, [1, labelCount]) #[-1, 1]
  plt.scatter(plot_x, plot_y, color='b', label='food')

  plot_x, plot_y = labelNums, corr[27]
  plot_x = np.reshape(plot_x, [1, labelCount]) #
  plot_y = np.reshape(plot_y, [1, labelCount]) #[-1, 1]
  plt.scatter(plot_x, plot_y, color='y', label='age')
  plt.xlabel("Dialogue Lines")
  plt.ylabel("STS (Correlation; 1 = same line)")
  plt.legend(loc ="lower right")

### ///-----------------------< MODEL Definition AND INPUT DATA >-----------------------\\\ ###
#---------------------------------------------------------------------------------------------#
# Here most of the magic happens. The input data is also in here and you can edit it to your
# heart's content. First input is the message or label itself; the lest are the properties.
#
# First property is Attitude which weights from positive 2 to negative -2. 0 Is neutral.
# Everything in between are degrees of positives and negatives. This is to indicate the mood
# can swing either way to change the dynamic of the conversation. Else the mood shouldn't sway.
#
# Second property is the type of message it is. S is Statement; Q is Question; A is Answer. 
#---------------------------------------------------------------------------------------------#

def run_and_plot_similarity(messages_, attitude_, type_):
  message_embeddings_ = embed(messages_)
  plot_similarity(messages_, message_embeddings_, 90)
  print_similarity(messages_, attitude_, type_ ,message_embeddings_)

def run_and_plot_visualization(messages_, attitude_, type_):
  message_embeddings_ = embed(messages_)
  plot_visualization(messages_, message_embeddings_, 90)
  #print_similarity(messages_, attitude_, type_ ,message_embeddings_)


messages = [
    # Smartphones
    "I like my phone.", "2", "S",
    "My phone is not good.", "-2", "S",
    "What is wrong with your phone?", "-2", "Q",
    "Good to see that you are enjoying your phone!", "2", "S",
    "Your cellphone looks great.", "2", "S",
    "Your cellphone looks better than mine.", "1", "S",
    "Thanks, my cellphone is also brand new!", "2", "A",
    "Thanks, but my cellphone is not as good as yours.", "1", "A",

    
    # Snow
    "Will it snow tomorrow?", "0", "Q",
    "I don't know, really. Do you think it will snow?", "0", "A",
    "I believe it will snow.", "0", "A",
    "I honestly just hope the snow won't be deep...", "-2", "A",
    "I am not so sure if it will snow.", "0", "A",
    "Yeah, there will be a blizzard soon.", "0", "A",
    "I hope you are dressed for the cold.", "0", "S",
    "I can't wait playing in the snow.", "2", "S",
    "I hate the cold...", "-2", "S",

    # Weather
    "Recently, a lot of hurricanes have hit the US.", "-2", "S",
    "Global warming is real.", "-2", "S",

    # Food and health
    "An apple a day, keeps the doctors away.", "2", "S",
    "Eating strawberries is healthy.", "2", "S",
    "I think strawberries are my favorite fruit.", "2", "S",
    "I would say, strawberries comes as a close second for me.", "2", "A",
    "I find strawberries to be overrated.", "-2", "S",
    "You talk an awful lot about strawberries...", "-2", "A",
    "Maybe you should try other fruits than just strawberries.", "-2", "A",
    "Is paleo better than keto?", "0", "Q",

    # Asking about age
    "How old are you?", "0", "Q",
    "My age is no concern of yours.", "-2", "A",
    "What are you - 12?", "-2", "Q",
    "I'm sure you could ask for something better than asking about my age.", "-2", "A",
    "What is your age?", "0", "Q",
]

### ///------------------------< PARTITION MESSAGE ARRAY BY TYPE >------------------------\\\ ###
#---------------------------------------------------------------------------------------------#
# Since the author should have complete overview of the properties of the dialogue lines,
# I made all input data able to be stored in a single CSV file. To transform this into a proper
# dataframe, they need to be partitioned correctly. Even then, they need to be seperated for
# Universal Sentence Encoder to work without the properties.
#---------------------------------------------------------------------------------------------#

messagesOnlyPrePass = messages
attitudeOnlyPrePass = messages
typeOnlyPrePass = messages

messagesOnly = []
for messagesOnlyPrePass in messagesOnlyPrePass[::3]:
   messagesOnly.append(messagesOnlyPrePass)
   #print("Printing messagesOnly...")
   #print(messagesOnly)

attitudeOnly = []
for attitudeOnlyPrePass in attitudeOnlyPrePass[1::3]:
   attitudeOnly.append(attitudeOnlyPrePass)
   #print("Printing attitudeOnly...")
   #print(attitudeOnly)

typeOnly = []
for typeOnlyPrePass in typeOnlyPrePass[2::3]:
   typeOnly.append(typeOnlyPrePass)
   #print("Printing typeOnly...")
   #print(typeOnly)


### ///--------------------< MODEL EXECUTION AND OUTPUT FUNCTIONS >---------------------\\\ ###
#---------------------------------------------------------------------------------------------#
# Simply executes everything defined so far. Underwhelmingly short.
#---------------------------------------------------------------------------------------------#

run_and_plot_similarity(messagesOnly, attitudeOnly, typeOnly)
plt.subplots_adjust(left=.36, bottom=.4, right=1, top=.92, wspace=.44, hspace=.22)
plt.show()

run_and_plot_visualization(messagesOnly, attitudeOnly, typeOnly)
plt.show()


### ///--------------------< EVALUATE SEMANTIC TEXTUAL SIMILARITY >--------------------\\\ ###
#---------------------------------------------------------------------------------------------#
# As documented in the paper, STS Benchmark is one of the trained dataset USE is based of.
# The correlation coefficient we get can be compared to the evaluation in the paper USE_T
# which lands around 0.814 / 0.782.
# 
# Comparing the correlation coefficient with the same classification formula documented in
# the paper, we get 0.803, so the value is within expected parameters. All within reasonable p-value.
# 
# STS Benchmark includes both a development set (sts_dev.CSV) and a test set (sts_stest.CSV)
# Similar as to what they documented in the paper.
#
# This is also the evaluation recommeneded by Tensorflow to evaluate the STS of the model
#---------------------------------------------------------------------------------------------#

# Load up datasets
sts_dataset = tf.keras.utils.get_file(
    fname="Stsbenchmark.tar.gz",
    origin="http://ixa2.si.ehu.es/stswiki/images/4/48/Stsbenchmark.tar.gz",
    extract=True)
sts_dev = pd.read_table(
    os.path.join(os.path.dirname(sts_dataset), "stsbenchmark", "sts-dev.csv"),
    on_bad_lines='warn',
    skip_blank_lines=True,
    usecols=[4, 5, 6],
    names=["sim", "sent_1", "sent_2"])
sts_test = pd.read_table(
    os.path.join(
        os.path.dirname(sts_dataset), "stsbenchmark", "sts-test.csv"),
    on_bad_lines='warn',
    quoting=csv.QUOTE_NONE,
    skip_blank_lines=True,
    usecols=[4, 5, 6],
    names=["sim", "sent_1", "sent_2"])
# cleanup some NaN values in sts_dev
sts_dev = sts_dev[[isinstance(s, str) for s in sts_dev['sent_2']]]


sts_data = sts_dev #@param ["sts_dev", "sts_test"] {type:"raw"}

def run_sts_benchmark(batch):
  sts_encode1 = tf.nn.l2_normalize(embed(tf.constant(batch['sent_1'].tolist())), axis=1)
  sts_encode2 = tf.nn.l2_normalize(embed(tf.constant(batch['sent_2'].tolist())), axis=1)
  cosine_similarities = tf.reduce_sum(tf.multiply(sts_encode1, sts_encode2), axis=1)
  clip_cosine_similarities = tf.clip_by_value(cosine_similarities, -1.0, 1.0)
  scores = 1.0 - tf.acos(clip_cosine_similarities) / math.pi
  """Returns the similarity scores"""
  return scores

dev_scores = sts_data['sim'].tolist()
scores = []
for batch in np.array_split(sts_data, 10):
  scores.extend(run_sts_benchmark(batch))

pearson_correlation = scipy.stats.pearsonr(scores, dev_scores)
#print("Printing pearson_correlation ...")
#print(pearson_correlation)
print('\n\nEvaluate with STS Benchmark ...\nPearson correlation coefficient = {0}\np-value = {1}\n\n\n'.format(
    pearson_correlation[0], pearson_correlation[1]))
