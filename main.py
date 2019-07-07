import sys
import os
import jagen_will.preproc.tuyau as tuy
import jagen_will.preproc.features_extract as fex
import fasttext
import pandas
import json
# from importlib import reload
# tuy = reload(tuy)
#import json , json.dump, file et object, json.load sur des files, dumps et loads sur des str
#import json

# TODO: eliminate features that occur only n times ?
# Do the Moisl Selection ?
# Z-scores, etc. ?
# Vector-length normalisation ?

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action="store", help="optional list of features in json", default=False)
    parser.add_argument('-t', action='store', help="types of features (words or chars)", type=str)
    parser.add_argument('-n', action='store', help="n grams lengths (default 1)", default=1, type=int)
    parser.add_argument('--z_scores', action='store_true', help="Use z-scores?", default=False)
    parser.add_argument('-s', nargs='+', help="paths to files")
    args = parser.parse_args()

    model = fasttext.load_model("jagen_will/preproc/models/lid.176.bin")

    print(".......loading texts.......")

    myTexts = tuy.load_texts(args.s, model)

    print(".......getting features.......")

    if not args.f:
        my_feats = fex.get_feature_list(myTexts, feats=args.t, n=args.n, relFreqs=True)
        # and now, cut at around rank k
        k = 5000
        val = my_feats[k][1]
        my_feats = [m for m in my_feats if m[1] >= val]

        # with open("feature_list.json", "w") as out:
        #    out.write(json.dumps(my_feats))

    else:
        print(".......loading preexisting feature list.......")
        with open(args.f, 'r') as f:
            my_feats = json.loads(f.read())

    print(".......getting counts.......")

    feat_list = [m[0] for m in my_feats]
    myTexts = fex.get_counts(myTexts, feat_list=feat_list, feats=args.t, n=args.n, relFreqs=True)

    unique_texts = [text["name"] for text in myTexts]

    print(".......feeding data frame.......")
    feats = pandas.DataFrame(columns=list(feat_list), index=unique_texts)

    for text in myTexts:

        local_freqs = []

        for word in feat_list:
            if word not in text["wordCounts"].keys():
                local_freqs.append(0)

            else:
                local_freqs.append(text["wordCounts"][word])

        feats.loc[text["name"]] = local_freqs

    print(".......applying normalisations.......")
    # And here is the place to implement selection and normalisation
    if args.z_scores:
        feat_stats = pandas.DataFrame(columns=["mean", "std"], index=list(feat_list))
        feat_stats.loc[:,"mean"] = list(feats.mean(axis=0))
        feat_stats.loc[:, "std"] = list(feats.std(axis=0))
        feat_stats.to_csv("feat_stats.csv")

        for col in list(feats.columns):
            feats[col] = (feats[col] - feats[col].mean()) / feats[col].std()

        # TODO: vector-length normalisation?

    print(".......saving results.......")
    # frequence based selection
    # WOW, pandas is a great tool, almost as good as using R
    # But confusing as well: boolean selection works on rows by default
    # were elsewhere it works on columns
    # take only rows where the number of values above 0 is superior to two
    # (i.e. appears in at least two texts)
    #feats = feats.loc[:, feats[feats > 0].count() > 2]

    metadata = pandas.DataFrame(columns=['author', 'lang'], index=unique_texts, data =
                                [[t["aut"], t["lang"]] for t in myTexts])

    pandas.concat([metadata, feats], axis=1).to_csv("feats_tests.csv")


