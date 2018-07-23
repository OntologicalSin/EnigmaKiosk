import json, nltk, os.path
import numpy as np
from nltk.stem import PorterStemmer
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Embedding, Dropout
from keras_preprocessing import sequence

batch_size = 9
maxLength = 10
posList = [
    "CC",
    "CD",
    "DT",
    "EX",
    "FW",
    "IN",
    "JJ",
    "JJR",
    "JJS",
    "LS",
    "MD",
    "NN",
    "NNS",
    "NNP",
    "NNPS",
    "PDT",
    "POS",
    "PRP",
    "PRP$",
    "RB",
    "RBR",
    "RBS",
    "RP",
    "TO",
    "UH",
    "VB",
    "VBD",
    "VBG",
    "VBN",
    "VBP",
    "VBZ",
    "WDT",
    "WP",
    "WP$",
    "WRB",
]

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
porter = PorterStemmer()


def preprocess(cmd):
    tempinputs = []
    for word in nltk.word_tokenize(cmd):
        tempinputs.append(porter.stem(word))
    tempinputs = [posList.index(I[1]) for I in nltk.pos_tag(tempinputs)]
    return tempinputs


if not os.path.isfile("nlp.h5"):
    model = Sequential()
    model.add(Embedding(len(posList) + 1, 32, input_length=maxLength))
    model.add(Dropout(0.25))
    model.add(LSTM(2 * 128))
    model.add(Dropout(0.25))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(loss="binary_crossentropy", optimizer="adam")
    # expected input data shape: (batch_size, timesteps, data_dim) np.array((batch_size, 5, 1))
    inputs = []
    outputs = []
    tempinputs = []
    with open("training_data.json", "r") as Input:
        JsonFile = json.load(Input)
        for Set in JsonFile:
            tempinputs = []
            inputs.append(preprocess(Set))
            outputs.append(np.array([JsonFile[Set]]))
    inputs = sequence.pad_sequences(inputs, maxlen=maxLength)
    print(inputs)
    model.fit(inputs, np.array(outputs), batch_size=batch_size, epochs=25)
    model.save("nlp.h5")
else:
    model = load_model("nlp.h5")
print(model.summary())


nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def main(cmd):
    origcmd = cmd
    cmd = [preprocess(cmd)]
    cmd = sequence.pad_sequences(cmd, maxlen=maxLength)
    prediction = model.predict(cmd)
    cmd = [posList[i] for i in np.trim_zeros(cmd[0])]
    print(cmd)
    orders = []
    for i in range(len(cmd)):
        count = 1
        if cmd[i] is "DT":
            if origcmd.lower() in nums:
                count += nums.index(origcmd[i])
            orders.append([nltk.word_tokenize(origcmd)[i + 1], count])
    return prediction, orders


if __name__ == "__main__":
    while True:
        print(main(input("Try: ")))