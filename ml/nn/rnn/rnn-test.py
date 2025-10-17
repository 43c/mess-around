import string
import numpy as np
from pprint import pprint

'''
test some rnn concepts

this whole idea of keeping memory through hidden states, does this
not imply that in long sequences, memory of past events fall off?
check memory-hypothesis.py

some words
time step -> position in sequence
          -> comes from markov models maybe? since markov models =
             transition over "time"
BPTT -> back propagation through time
     -> basically propagating gradient through unrolled RNN sequence 
        one token at a time?

so from what i can understand

we have some input sequence X
our RNN is made up of chains of "cells"
each cell takes in two inputs:
- x_t, x_t in X           -- one single token at a certain time step (position in sequence)
- previous hidden state   -- the previous hidden state, this is how RNN keeps "memory"
'''
def main():
    _tiny_forward_test()

def _other_test():
    X, y, token_map = sample_Xy()
    print(X)
    print(y)
    pprint(token_map)

    # vocab count, determines size of word vector in one hot
    feature_vec_size = len(X[0][0])
    print(feature_vec_size)

def _tiny_forward_test():
    np.random.seed(41)

    n_feats = 3 # features per x
    n_hiddens = 4 # hidden layer size
    n_outputs = 2 # output size
    T = 5 # seq len

    X = np.random.randn(T, n_feats, 1) # ndarray of all tokens in sequence

    # init weights and bias
    Wxh = np.random.randn(n_hiddens, n_feats)
    Whh = np.random.randn(n_hiddens, n_hiddens)
    Why = np.random.randn(n_outputs, n_hiddens)
    bh = np.zeros((n_hiddens, 1))
    by = np.zeros((n_outputs, 1))


    # forward pass
    ys, hs = forward(X, Wxh, Whh, Why, bh, by)

    # apparently because of the way numpy broadcasts
    # (n, 1) + (n, ) -> (n, n)
    # might not be the way I want it to be
    print("shapes")

    print(f"x_t: {X[0].shape}")
    print(f"  h: {hs[0].shape}")
    print(f"  y: {ys[0].shape}")
    print(f"Wxh: {Wxh.shape}")
    print(f"Whh: {Whh.shape}")
    print(f"Why: {Why.shape}")
    print(f" bh: {bh.shape}")
    print(f" by: {by.shape}")


    print(type(X[0]), type(ys[0]), type(hs[0]))
    print()

    # TODO print this nicely
    for t in range(T):
        print(f"t={t}")
        print(f"  x_{t}={X[t]}")
        print(f"  y_{t}={ys[t]}")
        print(f"  h_{t}={hs[t]}")
        

def forward(X, Wxh, Whh, Why, bh, by):
    '''
    forward pass for one single sample x in X
    we need some h0 for the h going into our initial h

    need to determine
    - size of the hidden layer
    - size of the output layer

                         [y_t]
                           ^  
                           |
                         @ Why
                           |
    [h_(t-1)] --@ Whh--> [h_t] --@ Whh--> [h_(t+1)]
                           ^
                           |
                         @ Wxh
                           |
                         [x_t]

    This seems to be a general idea of our forward pass.

    Biases
    bh := bias for computing next hidden state
    by := bias for computing output

    Shapes
    h : (hiddens, 1)
    x : (feats, 1)
    y : (outputs, 1)

    Wab := Wab @ a = b

    Wxh : (hiddens, feats)
    Whh : (hiddens, hiddens)
    Why : (ys, hiddens)
    '''

    h0 = np.zeros((Whh.shape[1], 1)) # pre-init hidden state

    h = h0
    ys = []
    hs = []
    for x_t in X:
        h = np.tanh(np.dot(Wxh, x_t) + np.dot(Whh, h) + bh)
        hs.append(h)
        ys.append(np.dot(Why, h) + by)
    return ys, hs

def tokenize(sentence_string_list):
    return [clean(x).split() for x in sentence_string_list]

def clean(s):
    return s.strip(string.punctuation).lower()

def one_hot(sent_tokens_list):
    '''
    thoughts:
    result is sparse 
    all words orthogonal, no semantic capture
    would want to try word embedding stuff but would need more
    data
    '''
    vocab_idx = {}
    idx = 0

    # build vocabulary position map
    for sentence in sent_tokens_list:
        for word in sentence:
            if word not in vocab_idx:
                vocab_idx[word] = idx
                idx += 1
    
    # list of    = corpus of sentences
    # -> list of = sentence of words (feature list)
    # ---> lists = individual word feature list
    V = len(vocab_idx)
    X = []
    # do actual one hot encoding
    for sentence in sent_tokens_list:
        sent_feats = []
        for word in sentence:
            word_f = [0] * V
            word_f[vocab_idx[word]] = 1
            sent_feats.append(word_f)

        X.append(np.asarray(sent_feats))

    # return vocab idk for later use perhaps
    return X, vocab_idx

def mini_test():

    corpus = [
        "I'm having a good day today",
        "i hate going to school",
        "it's so damn hot today",
        "what on earth was she thinking?"
    ]

    tokens = tokenize(corpus)
    pprint(tokens)

    X, token_map = one_hot(tokens)
    pprint(X)

def sample_Xy():
    '''
    meme function just to test stuff out
    '''
    sentences = [
        {"text": "I'm having a good day today", "label": "positive"},
        {"text": "I hate going to school", "label": "negative"},
        {"text": "It's so damn hot today", "label": "negative"},
        {"text": "What on earth was she thinking?", "label": "negative"},
        {"text": "I love this new phone!", "label": "positive"},
        {"text": "This coffee tastes awful", "label": "negative"},
        {"text": "Can't wait for the weekend", "label": "positive"},
        {"text": "I'm so tired of this nonsense", "label": "negative"},
        {"text": "That was the best movie I've seen in years", "label": "positive"},
        {"text": "I’m not sure what to do anymore", "label": "negative"},
        {"text": "My cat just knocked over my plant again", "label": "neutral"},
        {"text": "Feeling grateful for my friends today", "label": "positive"},
        {"text": "Ugh, traffic was horrible this morning", "label": "negative"},
        {"text": "I think I nailed that interview", "label": "positive"},
        {"text": "This restaurant is overrated", "label": "negative"},
        {"text": "It’s raining again, of course", "label": "neutral"},
        {"text": "I’m so proud of my little brother", "label": "positive"},
        {"text": "Why does everything go wrong at once?", "label": "negative"},
        {"text": "I’m really enjoying this book", "label": "positive"},
        {"text": "I can’t believe how rude that guy was", "label": "negative"},
        {"text": "What a beautiful sunset", "label": "positive"},
        {"text": "I just want to go home and sleep", "label": "neutral"},
        {"text": "This is exactly what I needed today", "label": "positive"},
        {"text": "I’m so done with people right now", "label": "negative"},
        {"text": "Got a promotion! Feeling amazing!", "label": "positive"},
        {"text": "My laptop died again… great", "label": "negative"},
        {"text": "Dinner turned out perfect tonight", "label": "positive"},
        {"text": "That was such a waste of time", "label": "negative"},
        {"text": "I feel relaxed after that walk", "label": "positive"},
        {"text": "He really gets on my nerves sometimes", "label": "negative"},
        {"text": "Life’s been pretty good lately", "label": "positive"},
        {"text": "This headache won’t go away", "label": "negative"},
        {"text": "So excited for vacation next week!", "label": "positive"},
        {"text": "The customer service here is terrible", "label": "negative"},
        {"text": "My dog always makes me smile", "label": "positive"},
        {"text": "Why is everything so expensive?", "label": "negative"},
        {"text": "I finally finished that project!", "label": "positive"},
        {"text": "I’m freezing, this weather sucks", "label": "negative"},
        {"text": "That concert was incredible", "label": "positive"},
        {"text": "I’m not in the mood to talk", "label": "neutral"},
        {"text": "She’s the sweetest person I know", "label": "positive"},
        {"text": "I’m stuck in traffic again", "label": "negative"},
        {"text": "Today has been so productive", "label": "positive"},
        {"text": "I feel like giving up", "label": "negative"},
        {"text": "What a lovely surprise!", "label": "positive"},
        {"text": "This app keeps crashing", "label": "negative"},
        {"text": "I can’t stop laughing at this meme", "label": "positive"},
        {"text": "My stomach hurts from eating too much", "label": "neutral"},
        {"text": "I miss my family so much", "label": "negative"},
        {"text": "He did such a great job on that presentation", "label": "positive"},
        {"text": "This song gives me chills every time", "label": "positive"},
        {"text": "Why can’t people just be kind?", "label": "negative"},
        {"text": "It’s too early for this nonsense", "label": "neutral"},
        {"text": "Finally got some good news today!", "label": "positive"},
        {"text": "I regret saying that immediately", "label": "negative"},
        {"text": "My internet is so slow, it’s painful", "label": "negative"},
        {"text": "I’m in such a good mood today", "label": "positive"},
        {"text": "That was completely unnecessary", "label": "negative"},
        {"text": "I could really use a nap right now", "label": "neutral"},
        {"text": "She always makes me laugh", "label": "positive"},
        {"text": "This weather is perfect for a picnic", "label": "positive"},
        {"text": "I’m so frustrated with myself", "label": "negative"},
        {"text": "We had an amazing time last night", "label": "positive"},
        {"text": "Nothing ever goes according to plan", "label": "negative"},
        {"text": "I’m feeling much better today", "label": "positive"},
        {"text": "This movie made me cry", "label": "negative"},
        {"text": "Why does this always happen to me?", "label": "negative"},
        {"text": "I’m so proud of what we accomplished", "label": "positive"},
        {"text": "That food was disgusting", "label": "negative"},
        {"text": "Can’t believe I forgot my wallet again", "label": "neutral"},
        {"text": "I’m in love with this city", "label": "positive"},
        {"text": "That joke was hilarious", "label": "positive"},
        {"text": "I just want to disappear for a while", "label": "negative"},
        {"text": "This is the best day ever!", "label": "positive"},
        {"text": "I’m getting really anxious about tomorrow", "label": "negative"},
        {"text": "He’s such a good listener", "label": "positive"},
        {"text": "I’m so done with this job", "label": "negative"},
        {"text": "The view from here is breathtaking", "label": "positive"},
        {"text": "I can’t believe how cold it is", "label": "neutral"},
        {"text": "I feel like I could take on the world", "label": "positive"},
        {"text": "That was incredibly disappointing", "label": "negative"},
        {"text": "I’m so thankful for everyone’s support", "label": "positive"},
        {"text": "Why did I even bother?", "label": "negative"},
        {"text": "This place is so peaceful", "label": "positive"},
        {"text": "I need a break from everything", "label": "neutral"},
        {"text": "I’m feeling optimistic about the future", "label": "positive"},
        {"text": "That service was awful", "label": "negative"},
        {"text": "She made my day with that message", "label": "positive"},
        {"text": "I’m running late again, as usual", "label": "neutral"},
        {"text": "The food smells amazing", "label": "positive"},
        {"text": "I can’t stand when people lie", "label": "negative"},
        {"text": "He’s always so positive about everything", "label": "positive"},
        {"text": "That was such a fun experience", "label": "positive"},
        {"text": "I feel terrible for forgetting her birthday", "label": "negative"},
        {"text": "This is exactly what I was hoping for", "label": "positive"},
        {"text": "I’m really disappointed in the outcome", "label": "negative"},
        {"text": "Today has been full of good vibes", "label": "positive"},
        {"text": "That was the worst experience ever", "label": "negative"},
        {"text": "I can’t believe how lucky I am", "label": "positive"},
        {"text": "Everything hurts, I’m so exhausted", "label": "negative"},
        {"text": "That compliment made my whole day", "label": "positive"},
        {"text": "I really need a vacation", "label": "neutral"}
    ]

    sentences_only = [sent["text"] for sent in sentences]

    def label_to_y(label):
        match label:
            case "negative":
                return -1
            case "neutral":
                return 0
            case "positive":
                return 1

    y = [label_to_y(sent["label"]) for sent in sentences]

    X, token_map = one_hot(tokenize(sentences_only))

    return X, np.asarray(y), token_map

if __name__ == "__main__":
    main()