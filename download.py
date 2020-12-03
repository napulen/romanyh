from urllib.request import urlretrieve
from urllib.parse import quote
import os

datasets = {
    "ABC": {
        "baseurl_annotations": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/ABC/",
        "baseurl_scores": "https://raw.githubusercontent.com/DCMLab/ABC/master/data/mscx/",
        "files": [
            {
                "annotation": "op127_mov1.txt",
                "score": "op. 127 No. 12/op127_no12_mov1.mscx",
            },
            {
                "annotation": "op127_mov2.txt",
                "score": "op. 127 No. 12/op127_no12_mov2.mscx",
            },
            {
                "annotation": "op127_mov3.txt",
                "score": "op. 127 No. 12/op127_no12_mov3.mscx",
            },
            {
                "annotation": "op127_mov4.txt",
                "score": "op. 127 No. 12/op127_no12_mov4.mscx",
            },
            {
                "annotation": "op130_mov1.txt",
                "score": "op. 130 No. 13/op130_no13_mov1.mscx",
            },
            {
                "annotation": "op130_mov2.txt",
                "score": "op. 130 No. 13/op130_no13_mov2.mscx",
            },
            {
                "annotation": "op130_mov3.txt",
                "score": "op. 130 No. 13/op130_no13_mov3.mscx",
            },
            {
                "annotation": "op130_mov4.txt",
                "score": "op. 130 No. 13/op130_no13_mov4.mscx",
            },
            {
                "annotation": "op130_mov5.txt",
                "score": "op. 130 No. 13/op130_no13_mov5.mscx",
            },
            {
                "annotation": "op130_mov6.txt",
                "score": "op. 130 No. 13/op130_no13_mov6.mscx",
            },
            {
                "annotation": "op131_mov1.txt",
                "score": "op. 131 No. 14/op131_no14_mov1.mscx",
            },
            {
                "annotation": "op131_mov2.txt",
                "score": "op. 131 No. 14/op131_no14_mov2.mscx",
            },
            {
                "annotation": "op131_mov3.txt",
                "score": "op. 131 No. 14/op131_no14_mov3.mscx",
            },
            {
                "annotation": "op131_mov4.txt",
                "score": "op. 131 No. 14/op131_no14_mov4.mscx",
            },
            {
                "annotation": "op131_mov5.txt",
                "score": "op. 131 No. 14/op131_no14_mov5.mscx",
            },
            {
                "annotation": "op131_mov6.txt",
                "score": "op. 131 No. 14/op131_no14_mov6.mscx",
            },
            {
                "annotation": "op131_mov7.txt",
                "score": "op. 131 No. 14/op131_no14_mov7.mscx",
            },
            {
                "annotation": "op132_mov1.txt",
                "score": "op. 132 No. 15/op132_no15_mov1.mscx",
            },
            {
                "annotation": "op132_mov2.txt",
                "score": "op. 132 No. 15/op132_no15_mov2.mscx",
            },
            {
                "annotation": "op132_mov3.txt",
                "score": "op. 132 No. 15/op132_no15_mov3.mscx",
            },
            {
                "annotation": "op132_mov4.txt",
                "score": "op. 132 No. 15/op132_no15_mov4.mscx",
            },
            {
                "annotation": "op132_mov5.txt",
                "score": "op. 132 No. 15/op132_no15_mov5.mscx",
            },
            {
                "annotation": "op135_mov1.txt",
                "score": "op. 135 No. 16/op135_no16_mov1.mscx",
            },
            {
                "annotation": "op135_mov2.txt",
                "score": "op. 135 No. 16/op135_no16_mov2.mscx",
            },
            {
                "annotation": "op135_mov3.txt",
                "score": "op. 135 No. 16/op135_no16_mov3.mscx",
            },
            {
                "annotation": "op135_mov4.txt",
                "score": "op. 135 No. 16/op135_no16_mov4.mscx",
            },
            {
                "annotation": "op18_no1_mov1.txt",
                "score": "op. 18 No. 1/op18_no1_mov1.mscx",
            },
            {
                "annotation": "op18_no1_mov2.txt",
                "score": "op. 18 No. 1/op18_no1_mov2.mscx",
            },
            {
                "annotation": "op18_no1_mov3.txt",
                "score": "op. 18 No. 1/op18_no1_mov3.mscx",
            },
            {
                "annotation": "op18_no1_mov4.txt",
                "score": "op. 18 No. 1/op18_no1_mov4.mscx",
            },
            {
                "annotation": "op18_no2_mov1.txt",
                "score": "op. 18 No. 2/op18_no2_mov1.mscx",
            },
            {
                "annotation": "op18_no2_mov2.txt",
                "score": "op. 18 No. 2/op18_no2_mov2.mscx",
            },
            {
                "annotation": "op18_no2_mov3.txt",
                "score": "op. 18 No. 2/op18_no2_mov3.mscx",
            },
            {
                "annotation": "op18_no2_mov4.txt",
                "score": "op. 18 No. 2/op18_no2_mov4.mscx",
            },
            {
                "annotation": "op18_no3_mov1.txt",
                "score": "op. 18 No. 3/op18_no3_mov1.mscx",
            },
            {
                "annotation": "op18_no3_mov2.txt",
                "score": "op. 18 No. 3/op18_no3_mov2.mscx",
            },
            {
                "annotation": "op18_no3_mov3.txt",
                "score": "op. 18 No. 3/op18_no3_mov3.mscx",
            },
            {
                "annotation": "op18_no3_mov4.txt",
                "score": "op. 18 No. 3/op18_no3_mov4.mscx",
            },
            {
                "annotation": "op18_no4_mov1.txt",
                "score": "op. 18 No. 4/op18_no4_mov1.mscx",
            },
            {
                "annotation": "op18_no4_mov2.txt",
                "score": "op. 18 No. 4/op18_no4_mov2.mscx",
            },
            {
                "annotation": "op18_no4_mov3.txt",
                "score": "op. 18 No. 4/op18_no4_mov3.mscx",
            },
            {
                "annotation": "op18_no4_mov4.txt",
                "score": "op. 18 No. 4/op18_no4_mov4.mscx",
            },
            {
                "annotation": "op18_no5_mov1.txt",
                "score": "op. 18 No. 5/op18_no5_mov1.mscx",
            },
            {
                "annotation": "op18_no5_mov2.txt",
                "score": "op. 18 No. 5/op18_no5_mov2.mscx",
            },
            {
                "annotation": "op18_no5_mov3.txt",
                "score": "op. 18 No. 5/op18_no5_mov3.mscx",
            },
            {
                "annotation": "op18_no5_mov4.txt",
                "score": "op. 18 No. 5/op18_no5_mov4.mscx",
            },
            {
                "annotation": "op18_no6_mov1.txt",
                "score": "op. 18 No. 6/op18_no6_mov1.mscx",
            },
            {
                "annotation": "op18_no6_mov2.txt",
                "score": "op. 18 No. 6/op18_no6_mov2.mscx",
            },
            {
                "annotation": "op18_no6_mov3.txt",
                "score": "op. 18 No. 6/op18_no6_mov3.mscx",
            },
            {
                "annotation": "op18_no6_mov4.txt",
                "score": "op. 18 No. 6/op18_no6_mov4.mscx",
            },
            {
                "annotation": "op59_no1_mov1.txt",
                "score": "op. 59 No. 7/op59_no7_mov1.mscx",
            },
            {
                "annotation": "op59_no1_mov2.txt",
                "score": "op. 59 No. 7/op59_no7_mov2.mscx",
            },
            {
                "annotation": "op59_no1_mov3.txt",
                "score": "op. 59 No. 7/op59_no7_mov3.mscx",
            },
            {
                "annotation": "op59_no1_mov4.txt",
                "score": "op. 59 No. 7/op59_no7_mov4.mscx",
            },
            {
                "annotation": "op59_no2_mov1.txt",
                "score": "op. 59 No. 8/op59_no8_mov1.mscx",
            },
            {
                "annotation": "op59_no2_mov2.txt",
                "score": "op. 59 No. 8/op59_no8_mov2.mscx",
            },
            {
                "annotation": "op59_no2_mov3.txt",
                "score": "op. 59 No. 8/op59_no8_mov3.mscx",
            },
            {
                "annotation": "op59_no2_mov4.txt",
                "score": "op. 59 No. 8/op59_no8_mov4.mscx",
            },
            {
                "annotation": "op59_no3_mov1.txt",
                "score": "op. 59 No. 9/op59_no9_mov1.mscx",
            },
            {
                "annotation": "op59_no3_mov2.txt",
                "score": "op. 59 No. 9/op59_no9_mov2.mscx",
            },
            {
                "annotation": "op59_no3_mov3.txt",
                "score": "op. 59 No. 9/op59_no9_mov3.mscx",
            },
            {
                "annotation": "op59_no3_mov4.txt",
                "score": "op. 59 No. 9/op59_no9_mov4.mscx",
            },
            {
                "annotation": "op74_mov1.txt",
                "score": "op. 74 No. 10/op74_no10_mov1.mscx",
            },
            {
                "annotation": "op74_mov2.txt",
                "score": "op. 74 No. 10/op74_no10_mov2.mscx",
            },
            {
                "annotation": "op74_mov3.txt",
                "score": "op. 74 No. 10/op74_no10_mov3.mscx",
            },
            {
                "annotation": "op74_mov4.txt",
                "score": "op. 74 No. 10/op74_no10_mov4.mscx",
            },
            {
                "annotation": "op95_mov1.txt",
                "score": "op. 95 No. 11/op95_no11_mov1.mscx",
            },
            {
                "annotation": "op95_mov2.txt",
                "score": "op. 95 No. 11/op95_no11_mov2.mscx",
            },
            {
                "annotation": "op95_mov3.txt",
                "score": "op. 95 No. 11/op95_no11_mov3.mscx",
            },
            {
                "annotation": "op95_mov4.txt",
                "score": "op. 95 No. 11/op95_no11_mov4.mscx",
            },
        ],
    },
    "m21BachChorales": {
        "baseurl_annotations": "https://raw.githubusercontent.com/cuthbertLab/music21/master/music21/corpus/bach/choraleAnalyses/",
        "baseurl_scores": "",
        "files": [
            {"annotation": "riemenschneider001.rntxt", "score": ""},
            {"annotation": "riemenschneider002.rntxt", "score": ""},
            {"annotation": "riemenschneider003.rntxt", "score": ""},
            {"annotation": "riemenschneider004.rntxt", "score": ""},
            {"annotation": "riemenschneider005.rntxt", "score": ""},
            {"annotation": "riemenschneider006.rntxt", "score": ""},
            {"annotation": "riemenschneider007.rntxt", "score": ""},
            {"annotation": "riemenschneider008.rntxt", "score": ""},
            {"annotation": "riemenschneider009.rntxt", "score": ""},
            {"annotation": "riemenschneider010.rntxt", "score": ""},
            {"annotation": "riemenschneider011.rntxt", "score": ""},
            {"annotation": "riemenschneider012.rntxt", "score": ""},
            {"annotation": "riemenschneider013.rntxt", "score": ""},
            {"annotation": "riemenschneider014.rntxt", "score": ""},
            {"annotation": "riemenschneider015.rntxt", "score": ""},
            {"annotation": "riemenschneider016.rntxt", "score": ""},
            {"annotation": "riemenschneider017.rntxt", "score": ""},
            {"annotation": "riemenschneider018.rntxt", "score": ""},
            {"annotation": "riemenschneider019.rntxt", "score": ""},
            {"annotation": "riemenschneider020.rntxt", "score": ""},
        ],
    },
    "m21Monteverdi": {
        "baseurl_annotations": "https://raw.githubusercontent.com/cuthbertLab/music21/master/music21/corpus/monteverdi/",
        "baseurl_scores": "https://raw.githubusercontent.com/cuthbertLab/music21/master/music21/corpus/monteverdi/",
        "files": [
            {"annotation": "madrigal.3.1.rntxt", "score": "madrigal.3.1.mxl"},
            {
                "annotation": "madrigal.3.10.rntxt",
                "score": "madrigal.3.10.mxl",
            },
            {
                "annotation": "madrigal.3.11.rntxt",
                "score": "madrigal.3.11.mxl",
            },
            {
                "annotation": "madrigal.3.12.rntxt",
                "score": "madrigal.3.12.mxl",
            },
            {
                "annotation": "madrigal.3.13.rntxt",
                "score": "madrigal.3.13.mxl",
            },
            {
                "annotation": "madrigal.3.14.rntxt",
                "score": "madrigal.3.14.mxl",
            },
            {
                "annotation": "madrigal.3.15.rntxt",
                "score": "madrigal.3.15.mxl",
            },
            {
                "annotation": "madrigal.3.16.rntxt",
                "score": "madrigal.3.16.mxl",
            },
            {
                "annotation": "madrigal.3.17.rntxt",
                "score": "madrigal.3.17.mxl",
            },
            {
                "annotation": "madrigal.3.18.rntxt",
                "score": "madrigal.3.18.mxl",
            },
            {
                "annotation": "madrigal.3.19.rntxt",
                "score": "madrigal.3.19.mxl",
            },
            {"annotation": "madrigal.3.2.rntxt", "score": "madrigal.3.2.mxl"},
            {
                "annotation": "madrigal.3.20.rntxt",
                "score": "madrigal.3.20.mxl",
            },
            {"annotation": "madrigal.3.3.rntxt", "score": "madrigal.3.3.mxl"},
            {"annotation": "madrigal.3.4.rntxt", "score": "madrigal.3.4.mxl"},
            {"annotation": "madrigal.3.5.rntxt", "score": "madrigal.3.5.mxl"},
            {"annotation": "madrigal.3.6.rntxt", "score": "madrigal.3.6.mxl"},
            {"annotation": "madrigal.3.7.rntxt", "score": "madrigal.3.7.mxl"},
            {"annotation": "madrigal.3.8.rntxt", "score": "madrigal.3.8.mxl"},
            {"annotation": "madrigal.3.9.rntxt", "score": "madrigal.3.9.mxl"},
            {"annotation": "madrigal.4.1.rntxt", "score": "madrigal.4.1.mxl"},
            {
                "annotation": "madrigal.4.10.rntxt",
                "score": "madrigal.4.10.mxl",
            },
            {
                "annotation": "madrigal.4.11.rntxt",
                "score": "madrigal.4.11.mxl",
            },
            {
                "annotation": "madrigal.4.12.rntxt",
                "score": "madrigal.4.12.mxl",
            },
            {
                "annotation": "madrigal.4.13.rntxt",
                "score": "madrigal.4.13.mxl",
            },
            {
                "annotation": "madrigal.4.14.rntxt",
                "score": "madrigal.4.14.mxl",
            },
            {
                "annotation": "madrigal.4.15.rntxt",
                "score": "madrigal.4.15.mxl",
            },
            {
                "annotation": "madrigal.4.16.rntxt",
                "score": "madrigal.4.16.mxl",
            },
            {
                "annotation": "madrigal.4.17.rntxt",
                "score": "madrigal.4.17.mxl",
            },
            {
                "annotation": "madrigal.4.18.rntxt",
                "score": "madrigal.4.18.mxl",
            },
            {
                "annotation": "madrigal.4.19.rntxt",
                "score": "madrigal.4.19.mxl",
            },
            {"annotation": "madrigal.4.2.rntxt", "score": "madrigal.4.2.mxl"},
            {
                "annotation": "madrigal.4.20.rntxt",
                "score": "madrigal.4.20.mxl",
            },
            {"annotation": "madrigal.4.3.rntxt", "score": "madrigal.4.3.mxl"},
            {"annotation": "madrigal.4.4.rntxt", "score": "madrigal.4.4.mxl"},
            {"annotation": "madrigal.4.5.rntxt", "score": "madrigal.4.5.mxl"},
            {"annotation": "madrigal.4.6.rntxt", "score": "madrigal.4.6.mxl"},
            {"annotation": "madrigal.4.7.rntxt", "score": "madrigal.4.7.mxl"},
            {"annotation": "madrigal.4.8.rntxt", "score": "madrigal.4.8.mxl"},
            {"annotation": "madrigal.4.9.rntxt", "score": "madrigal.4.9.mxl"},
            {"annotation": "madrigal.5.1.rntxt", "score": "madrigal.5.1.mxl"},
            {"annotation": "madrigal.5.2.rntxt", "score": "madrigal.5.2.mxl"},
            {"annotation": "madrigal.5.3.rntxt", "score": "madrigal.5.3.mxl"},
            {"annotation": "madrigal.5.4.rntxt", "score": "madrigal.5.4.mxl"},
            {"annotation": "madrigal.5.5.rntxt", "score": "madrigal.5.5.mxl"},
            {"annotation": "madrigal.5.6.rntxt", "score": "madrigal.5.6.mxl"},
            {"annotation": "madrigal.5.7.rntxt", "score": "madrigal.5.7.mxl"},
            {"annotation": "madrigal.5.8.rntxt", "score": "madrigal.5.8.mxl"},
        ],
    },
    "BachPreludes": {
        "baseurl_annotations": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/Bach_Preludes/",
        "baseurl_scores": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/Bach_Preludes/",
        "files": [
            {"annotation": "1/human.txt", "score": "1/score.mxl"},
            {"annotation": "10/human.txt", "score": "10/score.mxl"},
            {"annotation": "11/human.txt", "score": "11/score.mxl"},
            {"annotation": "12/human.txt", "score": "12/score.mxl"},
            {"annotation": "13/human.txt", "score": "13/score.mxl"},
            {"annotation": "14/human.txt", "score": "14/score.mxl"},
            {"annotation": "15/human.txt", "score": "15/score.mxl"},
            {"annotation": "16/human.txt", "score": "16/score.mxl"},
            {"annotation": "17/human.txt", "score": "17/score.mxl"},
            {"annotation": "18/human.txt", "score": "18/score.mxl"},
            {"annotation": "19/human.txt", "score": "19/score.mxl"},
            {"annotation": "2/human.txt", "score": "2/score.mxl"},
            {"annotation": "20/human.txt", "score": "20/score.mxl"},
            {"annotation": "21/human.txt", "score": "21/score.mxl"},
            {"annotation": "22/human.txt", "score": "22/score.mxl"},
            {"annotation": "23/human.txt", "score": "23/score.mxl"},
            {"annotation": "24/human.txt", "score": "24/score.mxl"},
            {"annotation": "3/human.txt", "score": "3/score.mxl"},
            {"annotation": "4/human.txt", "score": "4/score.mxl"},
            {"annotation": "5/human.txt", "score": "5/score.mxl"},
            {"annotation": "6/human.txt", "score": "6/score.mxl"},
            {"annotation": "7/human.txt", "score": "7/score.mxl"},
            {"annotation": "8/human.txt", "score": "8/score.mxl"},
            {"annotation": "9/human.txt", "score": "9/score.mxl"},
        ],
    },
    "BeethovenSonatas": {
        "baseurl_annotations": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/Beethoven_Piano_Sonatas/",
        "baseurl_scores": "",
        "files": [
            {"annotation": "29op106(Hammerklavier)/movt1/analysis.txt", "score": ""},
            {"annotation": "24op78/movt1/analysis.txt", "score": ""},
            {"annotation": "10op14no2/movt1/analysis.txt", "score": ""},
            {"annotation": "31op110/movt1/analysis.txt", "score": ""},
            {"annotation": "3op2no3/movt1/analysis.txt", "score": ""},
            {"annotation": "18op31no3/movt1/analysis.txt", "score": ""},
            {"annotation": "25op79(SONATINA)/movt1/analysis.txt", "score": ""},
            {"annotation": "27op90/movt1/analysis.txt", "score": ""},
            {"annotation": "8op13(Pathetique)/movt1/analysis.txt", "score": ""},
            {"annotation": "19op49no1/movt1/analysis.txt", "score": ""},
            {"annotation": "23op57(APPASSIONATA)/movt1/analysis.txt", "score": ""},
            {"annotation": "16op31no1/movt1/analysis.txt", "score": ""},
            {"annotation": "1op2no1/movt1/analysis.txt", "score": ""},
            {"annotation": "32op111/movt1/analysis.txt", "score": ""},
            {"annotation": "22op54/movt1/analysis.txt", "score": ""},
            {"annotation": "2op2no2/movt1/analysis.txt", "score": ""},
            {"annotation": "28op101/movt1/analysis.txt", "score": ""},
            {"annotation": "14op27no2(Moonlight)/movt1/analysis.txt", "score": ""},
            {"annotation": "21op53/movt1/analysis.txt", "score": ""},
            {"annotation": "9op14no1/movt1/analysis.txt", "score": ""},
            {"annotation": "17op31no2/movt1/analysis.txt", "score": ""},
            {"annotation": "6op10no2/movt1/analysis.txt", "score": ""},
            {"annotation": "26op81a(LESADIEUX)/movt1/analysis.txt", "score": ""},
            {"annotation": "5op10no1/movt1/analysis.txt", "score": ""},
            {"annotation": "20op49no2/movt1/analysis.txt", "score": ""},
            {"annotation": "30op109/movt1/analysis.txt", "score": ""},
            {"annotation": "7op10no3/movt1/analysis.txt", "score": ""},
            {"annotation": "4op7/movt1/analysis.txt", "score": ""},
            {"annotation": "11op22/movt1/analysis.txt", "score": ""},
            {"annotation": "15op28(Pastorale)/movt1/analysis.txt", "score": ""},
            {"annotation": "12op26/movt1/analysis.txt", "score": ""},
            {"annotation": "13op27no1/movt1/analysis.txt", "score": ""},
        ],
    },
    "Grounds": {
        "baseurl_annotations": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/Grounds/",
        "baseurl_scores": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/Grounds/",
        "files": [
            {
                "annotation": "Purcell Sonata in G Minor Z807/human.txt",
                "score": "Purcell Sonata in G Minor Z807/score.mxl",
            },
            {
                "annotation": "Bach Crucifixus B Minor mass BWV232/human.txt",
                "score": "Bach Crucifixus B Minor mass BWV232/score.mxl",
            },
            {
                "annotation": "Purcell Chacony_(Chaconne)/human.txt",
                "score": "Purcell Chacony_(Chaconne)/score.mxl",
            },
        ],
    },
    "HaydnOp20": {
        "baseurl_annotations": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/HaydnOp20/",
        "baseurl_scores": "https://raw.githubusercontent.com/napulen/haydn_op20_harm/master/op20/",
        "files": [
            {"annotation": "op20n1-01.txt", "score": "1/i/op20n1-01.krn"},
            {"annotation": "op20n1-02.txt", "score": "1/ii/op20n1-02.krn"},
            {"annotation": "op20n1-03.txt", "score": "1/iii/op20n1-03.krn"},
            {"annotation": "op20n1-04.txt", "score": "1/iv/op20n1-04.krn"},
            {"annotation": "op20n2-01.txt", "score": "2/i/op20n2-01.krn"},
            {"annotation": "op20n2-02.txt", "score": "2/ii/op20n2-02.krn"},
            {"annotation": "op20n2-03.txt", "score": "2/iii/op20n2-03.krn"},
            {"annotation": "op20n2-04.txt", "score": "2/iv/op20n2-04.krn"},
            {"annotation": "op20n3-01.txt", "score": "3/i/op20n3-01.krn"},
            {"annotation": "op20n3-02.txt", "score": "3/ii/op20n3-02.krn"},
            {"annotation": "op20n3-03.txt", "score": "3/iii/op20n3-03.krn"},
            {"annotation": "op20n3-04.txt", "score": "3/iv/op20n3-04.krn"},
            {"annotation": "op20n4-01.txt", "score": "4/i/op20n4-01.krn"},
            {"annotation": "op20n4-02.txt", "score": "4/ii/op20n4-02.krn"},
            {"annotation": "op20n4-03.txt", "score": "4/iii/op20n4-03.krn"},
            {"annotation": "op20n4-04.txt", "score": "4/iv/op20n4-04.krn"},
            {"annotation": "op20n5-01.txt", "score": "5/i/op20n5-01.krn"},
            {"annotation": "op20n5-02.txt", "score": "5/ii/op20n5-02.krn"},
            {"annotation": "op20n5-03.txt", "score": "5/iii/op20n5-03.krn"},
            {"annotation": "op20n5-04.txt", "score": "5/iv/op20n5-04.krn"},
            {"annotation": "op20n6-01.txt", "score": "6/i/op20n6-01.krn"},
            {"annotation": "op20n6-02.txt", "score": "6/ii/op20n6-02.krn"},
            {"annotation": "op20n6-03.txt", "score": "6/iii/op20n6-03.krn"},
            {"annotation": "op20n6-04.txt", "score": "6/iv/op20n6-04.krn"},
        ],
    },
    "Misc": {
        "baseurl_annotations": "https://github.com/MarkGotham/When-in-Rome/blob/master/Corpus/Misc/",
        "baseurl_scores": "https://github.com/MarkGotham/When-in-Rome/blob/master/Corpus/Misc/",
        "files": [
            {
                "annotation": "Haydn Symphony 104 Movement 1/human.txt",
                "score": "Haydn Symphony 104 Movement 1/score.mxl",
            },
        ],
    },
    "OpenScore": {
        "baseurl_annotations": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/OpenScore-LiederCorpus/",
        "baseurl_scores": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/OpenScore-LiederCorpus/",
        "files": [
            {
                "annotation": "Brahms,_Johannes/6_Songs,_Op.3/3_Liebe_und_Frühling_II/analysis.txt",
                "score": "Brahms,_Johannes/6_Songs,_Op.3/3_Liebe_und_Frühling_II/analysis.txt",
            },
            {
                "annotation": "Brahms,_Johannes/7_Lieder,_Op.48/3_Liebesklage_des_Mädchens/analysis.txt",
                "score": "Brahms,_Johannes/7_Lieder,_Op.48/3_Liebesklage_des_Mädchens/analysis.txt",
            },
            {
                "annotation": "Chaminade,_Cécile/_/Amoroso/analysis.txt",
                "score": "Chaminade,_Cécile/_/Amoroso/analysis.txt",
            },
            {
                "annotation": "Chausson,_Ernest/7_Mélodies,_Op.2/7_Le_Colibri/analysis.txt",
                "score": "Chausson,_Ernest/7_Mélodies,_Op.2/7_Le_Colibri/analysis.txt",
            },
            {
                "annotation": "Coleridge-Taylor,_Samuel/_/Oh,_the_Summer/analysis.txt",
                "score": "Coleridge-Taylor,_Samuel/_/Oh,_the_Summer/analysis.txt",
            },
            {
                "annotation": "Franz,_Robert/6_Gesänge,_Op.14/5_Liebesfrühling/analysis.txt",
                "score": "Franz,_Robert/6_Gesänge,_Op.14/5_Liebesfrühling/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/3_Lieder/1_Sehnsucht/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/3_Lieder/1_Sehnsucht/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/1_Nach_Süden/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/1_Nach_Süden/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/2_Vorwurf/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/2_Vorwurf/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/3_Abendbild/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/3_Abendbild/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/4_Im_Herbste/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/4_Im_Herbste/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/5_Bergeslust/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/5_Lieder,_Op.10/5_Bergeslust/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/1_Schwanenlied/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/1_Schwanenlied/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/2_Wanderlied/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/2_Wanderlied/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/3_Warum_sind_denn_die_Rosen_so_blass/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/3_Warum_sind_denn_die_Rosen_so_blass/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/4_Mayenlied/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/4_Mayenlied/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/5_Morgenständchen/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/5_Morgenständchen/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/6_Gondellied/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.1/6_Gondellied/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/1_Die_Ersehnte/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/1_Die_Ersehnte/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/2_Ferne/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/2_Ferne/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/3_Der_Rosenkranz/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/3_Der_Rosenkranz/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/4_Die_frühen_Gräber/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/4_Die_frühen_Gräber/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/5_Der_Maiabend/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/5_Der_Maiabend/analysis.txt",
            },
            {
                "annotation": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/6_Die_Mainacht/analysis.txt",
                "score": "Hensel,_Fanny_(Mendelssohn)/6_Lieder,_Op.9/6_Die_Mainacht/analysis.txt",
            },
            {
                "annotation": "Holmès,_Augusta_Mary_Anne/Les_Heures/4_L’Heure_d’Azur/analysis.txt",
                "score": "Holmès,_Augusta_Mary_Anne/Les_Heures/4_L’Heure_d’Azur/analysis.txt",
            },
            {
                "annotation": "Jaëll,_Marie/4_Mélodies/1_À_toi/analysis.txt",
                "score": "Jaëll,_Marie/4_Mélodies/1_À_toi/analysis.txt",
            },
            {
                "annotation": "Lang,_Josephine/6_Lieder,_Op.25/4_Lied_(Immer_sich_rein_kindlich_erfreu’n)/analysis.txt",
                "score": "Lang,_Josephine/6_Lieder,_Op.25/4_Lied_(Immer_sich_rein_kindlich_erfreu’n)/analysis.txt",
            },
            {
                "annotation": "Mahler,_Gustav/Kindertotenlieder/2_Nun_seh’_ich_wohl,_warum_so_dunkle_Flammen/analysis.txt",
                "score": "Mahler,_Gustav/Kindertotenlieder/2_Nun_seh’_ich_wohl,_warum_so_dunkle_Flammen/analysis.txt",
            },
            {
                "annotation": "Mahler,_Gustav/Kindertotenlieder/4_Oft_denk’_ich,_sie_sind_nur_ausgegangen/analysis.txt",
                "score": "Mahler,_Gustav/Kindertotenlieder/4_Oft_denk’_ich,_sie_sind_nur_ausgegangen/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Sechs_Lieder_von_Novalis,_Op.4/5_Noch_ein_Bergmannslied/analysis.txt",
                "score": "Reichardt,_Louise/Sechs_Lieder_von_Novalis,_Op.4/5_Noch_ein_Bergmannslied/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Deutsche_und_Italiänische_Romantische_Gesänge/10_Ida_(aus_Ariels_Offenbarungen)/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Deutsche_und_Italiänische_Romantische_Gesänge/10_Ida_(aus_Ariels_Offenbarungen)/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/01_Frühlingsblumen/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/01_Frühlingsblumen/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/02_Der_traurige_Wanderer/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/02_Der_traurige_Wanderer/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/03_Die_Blume_der_Blumen/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/03_Die_Blume_der_Blumen/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/04_Wachtelwacht/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/04_Wachtelwacht/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/05_Betteley_der_Vögel/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/05_Betteley_der_Vögel/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/06_Kriegslied_des_Mays/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/06_Kriegslied_des_Mays/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/07_Die_Wiese/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/07_Die_Wiese/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/08_Kaeuzlein/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/08_Kaeuzlein/analysis.txt",
            },
            {
                "annotation": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/09_Hier_liegt_ein_Spielmann_begraben/analysis.txt",
                "score": "Reichardt,_Louise/Zwölf_Gesänge,_Op.3/09_Hier_liegt_ein_Spielmann_begraben/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Die_schöne_Müllerin,_D.795/12_Pause/analysis.txt",
                "score": "Schubert,_Franz/Die_schöne_Müllerin,_D.795/12_Pause/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Op.59/3_Du_bist_die_Ruh/analysis.txt",
                "score": "Schubert,_Franz/Op.59/3_Du_bist_die_Ruh/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/01_Liebesbotschaft/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/01_Liebesbotschaft/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/02_Kriegers_Ahnung/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/02_Kriegers_Ahnung/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/03_Frühlingssehnsucht/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/03_Frühlingssehnsucht/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/04_Ständchen/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/04_Ständchen/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/05_Aufenthalt/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/05_Aufenthalt/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/06_In_der_Ferne/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/06_In_der_Ferne/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/07_Abschied/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/07_Abschied/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/08_Der_Atlas/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/08_Der_Atlas/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/09_Ihr_Bild/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/09_Ihr_Bild/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/10_Das_Fischermädchen/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/10_Das_Fischermädchen/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/11_Die_Stadt/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/11_Die_Stadt/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/12_Am_Meer/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/12_Am_Meer/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/13_Der_Doppelgänger/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/13_Der_Doppelgänger/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Schwanengesang,_D.957/14_Die_Taubenpost/analysis.txt",
                "score": "Schubert,_Franz/Schwanengesang,_D.957/14_Die_Taubenpost/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/01_Gute_Nacht/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/02_Die_Wetterfahne/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/02_Die_Wetterfahne/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/03_Gefror’ne_Thränen/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/03_Gefror’ne_Thränen/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/04_Erstarrung/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/04_Erstarrung/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/05_Der_Lindenbaum/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/05_Der_Lindenbaum/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/06_Wasserfluth/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/06_Wasserfluth/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/07_Auf_dem_Flusse/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/07_Auf_dem_Flusse/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/08_Rückblick/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/08_Rückblick/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/09_Irrlicht/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/09_Irrlicht/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/10_Rast_(Spätere_Fassung)/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/10_Rast_(Spätere_Fassung)/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/11_Frühlingstraum/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/11_Frühlingstraum/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/12_Einsamkeit_(Urspruengliche_Fassung)/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/12_Einsamkeit_(Urspruengliche_Fassung)/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/13_Die_Post/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/13_Die_Post/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/14_Der_greise_Kopf/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/14_Der_greise_Kopf/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/15_Die_Kraehe/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/15_Die_Kraehe/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/16_Letzte_Hoffnung/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/16_Letzte_Hoffnung/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/17_Im_Dorfe/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/17_Im_Dorfe/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/18_Der_stuermische_Morgen/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/18_Der_stuermische_Morgen/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/19_Täuschung/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/19_Täuschung/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/20_Der_Wegweiser/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/20_Der_Wegweiser/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/21_Das_Wirthshaus/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/21_Das_Wirthshaus/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/22_Muth/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/22_Muth/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/23_Die_Nebensonnen/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/23_Die_Nebensonnen/analysis.txt",
            },
            {
                "annotation": "Schubert,_Franz/Winterreise,_D.911/24_Der_Leiermann_(Spätere_Fassung)/analysis.txt",
                "score": "Schubert,_Franz/Winterreise,_D.911/24_Der_Leiermann_(Spätere_Fassung)/analysis.txt",
            },
            {
                "annotation": "Schumann,_Clara/6_Lieder,_Op.13/1_Ich_stand_in_dunklen_Träumen/analysis.txt",
                "score": "Schumann,_Clara/6_Lieder,_Op.13/1_Ich_stand_in_dunklen_Träumen/analysis.txt",
            },
            {
                "annotation": "Schumann,_Clara/6_Lieder,_Op.13/2_Sie_liebten_sich_beide/analysis.txt",
                "score": "Schumann,_Clara/6_Lieder,_Op.13/2_Sie_liebten_sich_beide/analysis.txt",
            },
            {
                "annotation": "Schumann,_Clara/6_Lieder,_Op.13/3_Liebeszauber/analysis.txt",
                "score": "Schumann,_Clara/6_Lieder,_Op.13/3_Liebeszauber/analysis.txt",
            },
            {
                "annotation": "Schumann,_Clara/6_Lieder,_Op.13/6_Die_stille_Lotosblume/analysis.txt",
                "score": "Schumann,_Clara/6_Lieder,_Op.13/6_Die_stille_Lotosblume/analysis.txt",
            },
            {
                "annotation": "Schumann,_Clara/6_Lieder,_Op.23/4_Auf_einem_grünen_Hügel/analysis.txt",
                "score": "Schumann,_Clara/6_Lieder,_Op.23/4_Auf_einem_grünen_Hügel/analysis.txt",
            },
            {
                "annotation": "Schumann,_Clara/Lieder,_Op.12/04_Liebst_du_um_Schönheit/analysis.txt",
                "score": "Schumann,_Clara/Lieder,_Op.12/04_Liebst_du_um_Schönheit/analysis.txt",
            },
            {
                "annotation": "Schumann,_Clara/_/Die_gute_Nacht/analysis.txt",
                "score": "Schumann,_Clara/_/Die_gute_Nacht/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/01_Im_wunderschönen_Monat_Mai/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/01_Im_wunderschönen_Monat_Mai/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/02_Aus_meinen_Tränen_sprießen/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/02_Aus_meinen_Tränen_sprießen/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/03_Die_Rose,_die_Lilie/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/03_Die_Rose,_die_Lilie/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/04_Wenn_ich_in_deine_Augen_seh’/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/04_Wenn_ich_in_deine_Augen_seh’/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/05_Ich_will_meine_Seele_tauchen/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/05_Ich_will_meine_Seele_tauchen/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/06_Im_Rhein,_im_heiligen_Strome/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/06_Im_Rhein,_im_heiligen_Strome/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/07_Ich_grolle_nicht/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/07_Ich_grolle_nicht/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/08_Und_wüssten’s_die_Blumen/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/08_Und_wüssten’s_die_Blumen/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/09_Das_ist_ein_Flöten_und_Geigen/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/09_Das_ist_ein_Flöten_und_Geigen/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/10_Hör’_ich_das_Liedchen_klingen/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/10_Hör’_ich_das_Liedchen_klingen/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/11_Ein_Jüngling_liebt_ein_Mädchen/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/11_Ein_Jüngling_liebt_ein_Mädchen/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/12_Am_leuchtenden_Sommermorgen/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/12_Am_leuchtenden_Sommermorgen/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/13_Ich_hab’_im_Traum_geweinet/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/13_Ich_hab’_im_Traum_geweinet/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/14_Allnächtlich_im_Traume/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/14_Allnächtlich_im_Traume/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/15_Aus_alten_Märchen_winkt_es/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/15_Aus_alten_Märchen_winkt_es/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Dichterliebe,_Op.48/16_Die_alten,_bösen_Lieder/analysis.txt",
                "score": "Schumann,_Robert/Dichterliebe,_Op.48/16_Die_alten,_bösen_Lieder/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/1_Seit_ich_ihn_gesehen/analysis.txt",
                "score": "Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/1_Seit_ich_ihn_gesehen/analysis.txt",
            },
            {
                "annotation": "Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/3_Ich_kann’s_nicht_fassen/analysis.txt",
                "score": "Schumann,_Robert/Frauenliebe_und_Leben,_Op.42/3_Ich_kann’s_nicht_fassen/analysis.txt",
            },
            {
                "annotation": "Wolf,_Hugo/Eichendorff-Lieder/04_Das_Ständchen/analysis.txt",
                "score": "Wolf,_Hugo/Eichendorff-Lieder/04_Das_Ständchen/analysis.txt",
            },
            {
                "annotation": "Wolf,_Hugo/Eichendorff-Lieder/08_Nachtzauber/analysis.txt",
                "score": "Wolf,_Hugo/Eichendorff-Lieder/08_Nachtzauber/analysis.txt",
            },
            {
                "annotation": "Wolf,_Hugo/Eichendorff-Lieder/13_Der_Scholar/analysis.txt",
                "score": "Wolf,_Hugo/Eichendorff-Lieder/13_Der_Scholar/analysis.txt",
            },
            {
                "annotation": "Wolf,_Hugo/Eichendorff-Lieder/14_Der_verzweifelte_Liebhaber/analysis.txt",
                "score": "Wolf,_Hugo/Eichendorff-Lieder/14_Der_verzweifelte_Liebhaber/analysis.txt",
            },
            {
                "annotation": "Wolf,_Hugo/Eichendorff-Lieder/15_Unfall/analysis.txt",
                "score": "Wolf,_Hugo/Eichendorff-Lieder/15_Unfall/analysis.txt",
            },
            {
                "annotation": "Wolf,_Hugo/Eichendorff-Lieder/19_Die_Nacht/analysis.txt",
                "score": "Wolf,_Hugo/Eichendorff-Lieder/19_Die_Nacht/analysis.txt",
            },
            {
                "annotation": "Wolf,_Hugo/Eichendorff-Lieder/20_Waldmädchen/analysis.txt",
                "score": "Wolf,_Hugo/Eichendorff-Lieder/20_Waldmädchen/analysis.txt",
            },
        ],
    },
    "TAVERN": {
        "baseurl_annotations": "https://raw.githubusercontent.com/MarkGotham/When-in-Rome/master/Corpus/TAVERN/",
        "baseurl_scores": "https://raw.githubusercontent.com/jcdevaney/TAVERN/master/",
        "files": [
            {
                "annotation": "Beethoven/B063_A.txt",
                "score": "Beethoven/B063/Krn/Wo063.krn",
            },
            {
                "annotation": "Beethoven/B064_A.txt",
                "score": "Beethoven/B064/Krn/Wo064.krn",
            },
            {
                "annotation": "Beethoven/B065_A.txt",
                "score": "Beethoven/B065/Krn/Wo065.krn",
            },
            {
                "annotation": "Beethoven/B066_A.txt",
                "score": "Beethoven/B066/Krn/Wo066.krn",
            },
            {
                "annotation": "Beethoven/B068_A.txt",
                "score": "Beethoven/B068/Krn/Wo068.krn",
            },
            {
                "annotation": "Beethoven/B069_A.txt",
                "score": "Beethoven/B069/Krn/Wo069.krn",
            },
            {
                "annotation": "Beethoven/B070_A.txt",
                "score": "Beethoven/B070/Krn/Wo070.krn",
            },
            {
                "annotation": "Beethoven/B071_a.txt",
                "score": "Beethoven/B071/Krn/Wo071.krn",
            },
            {
                "annotation": "Beethoven/B072_A.txt",
                "score": "Beethoven/B072/Krn/Wo072.krn",
            },
            {
                "annotation": "Beethoven/B073_A.txt",
                "score": "Beethoven/B073/Krn/Wo073.krn",
            },
            {
                "annotation": "Beethoven/B075_A.txt",
                "score": "Beethoven/B075/Krn/Wo075.krn",
            },
            {"annotation": "Beethoven/B076_A.txt", "score": ""},
            {
                "annotation": "Beethoven/B077_A.txt",
                "score": "Beethoven/B077/Krn/Wo077.krn",
            },
            {
                "annotation": "Beethoven/B078_A.txt",
                "score": "Beethoven/B078/Krn/Wo078.krn",
            },
            {
                "annotation": "Beethoven/B080_A.txt",
                "score": "Beethoven/B080/Krn/Wo080.krn",
            },
            {
                "annotation": "Beethoven/Opus34_A.txt",
                "score": "Beethoven/Opus34/Krn/Opus34.krn",
            },
            {
                "annotation": "Beethoven/Opus76_A.txt",
                "score": "Beethoven/Opus76/Krn/Opus76.krn",
            },
            {
                "annotation": "Beethoven/B063_B.txt",
                "score": "Beethoven/B063/Krn/Wo063.krn",
            },
            {
                "annotation": "Beethoven/B064_B.txt",
                "score": "Beethoven/B064/Krn/Wo064.krn",
            },
            {
                "annotation": "Beethoven/B065_B.txt",
                "score": "Beethoven/B065/Krn/Wo065.krn",
            },
            {
                "annotation": "Beethoven/B066_B.txt",
                "score": "Beethoven/B066/Krn/Wo066.krn",
            },
            {
                "annotation": "Beethoven/B068_B.txt",
                "score": "Beethoven/B068/Krn/Wo068.krn",
            },
            {
                "annotation": "Beethoven/B069_B.txt",
                "score": "Beethoven/B069/Krn/Wo069.krn",
            },
            {
                "annotation": "Beethoven/B070_B.txt",
                "score": "Beethoven/B070/Krn/Wo070.krn",
            },
            {
                "annotation": "Beethoven/B071_B.txt",
                "score": "Beethoven/B071/Krn/Wo071.krn",
            },
            {
                "annotation": "Beethoven/B072_B.txt",
                "score": "Beethoven/B072/Krn/Wo072.krn",
            },
            {
                "annotation": "Beethoven/B073_B.txt",
                "score": "Beethoven/B073/Krn/Wo073.krn",
            },
            {
                "annotation": "Beethoven/B075_B.txt",
                "score": "Beethoven/B075/Krn/Wo075.krn",
            },
            {"annotation": "Beethoven/B076_B.txt", "score": ""},
            {
                "annotation": "Beethoven/B077_B.txt",
                "score": "Beethoven/B077/Krn/Wo077.krn",
            },
            {
                "annotation": "Beethoven/B078_B.txt",
                "score": "Beethoven/B078/Krn/Wo078.krn",
            },
            {
                "annotation": "Beethoven/B080_B.txt",
                "score": "Beethoven/B080/Krn/Wo080.krn",
            },
            {
                "annotation": "Beethoven/Opus34_B.txt",
                "score": "Beethoven/Opus34/Krn/Opus34.krn",
            },
            {
                "annotation": "Beethoven/Opus76_B.txt",
                "score": "Beethoven/Opus76/Krn/Opus76.krn",
            },
            {
                "annotation": "Mozart/K179_B.txt",
                "score": "Mozart/K179/Krn/K179.krn",
            },
            {
                "annotation": "Mozart/K501_A.txt",
                "score": "Mozart/K501/Krn/K501.krn",
            },
            {
                "annotation": "Mozart/K613_A.txt",
                "score": "Mozart/K613/Krn/K613.krn",
            },
            {
                "annotation": "Mozart/K573_B.txt",
                "score": "Mozart/K573/Krn/K573.krn",
            },
            {
                "annotation": "Mozart/K613_B.txt",
                "score": "Mozart/K613/Krn/K613.krn",
            },
            {
                "annotation": "Mozart/K501_B.txt",
                "score": "Mozart/K501/Krn/K501.krn",
            },
            {
                "annotation": "Mozart/K398_A.txt",
                "score": "Mozart/K398/Krn/K398.krn",
            },
            {
                "annotation": "Mozart/K025_B.txt",
                "score": "Mozart/K025/Krn/K025.krn",
            },
            {
                "annotation": "Mozart/K398_B.txt",
                "score": "Mozart/K398/Krn/K398.krn",
            },
            {
                "annotation": "Mozart/K265_A.txt",
                "score": "Mozart/K265/Krn/K265.krn",
            },
            {
                "annotation": "Mozart/K353_A.txt",
                "score": "Mozart/K353/Krn/K353.krn",
            },
            {
                "annotation": "Mozart/K354_B.txt",
                "score": "Mozart/K354/Krn/K354.krn",
            },
            {
                "annotation": "Mozart/K353_B.txt",
                "score": "Mozart/K353/Krn/K353.krn",
            },
            {
                "annotation": "Mozart/K354_A.txt",
                "score": "Mozart/K354/Krn/K354.krn",
            },
            {
                "annotation": "Mozart/K265_B.txt",
                "score": "Mozart/K265/Krn/K265.krn",
            },
            {
                "annotation": "Mozart/K455_A.txt",
                "score": "Mozart/K455/Krn/K455.krn",
            },
            {
                "annotation": "Mozart/K455_B.txt",
                "score": "Mozart/K455/Krn/K455.krn",
            },
            {
                "annotation": "Mozart/K179_A.txt",
                "score": "Mozart/K179/Krn/K179.krn",
            },
            {
                "annotation": "Mozart/K573_A.txt",
                "score": "Mozart/K573/Krn/K573.krn",
            },
            {
                "annotation": "Mozart/K025_A.txt",
                "score": "Mozart/K025/Krn/K025.krn",
            },
        ],
    },
}

datasetFolder = "dataset"

for datasetName, dataset in datasets.items():
    print(datasetName)
    baseurl_annotations = dataset["baseurl_annotations"]
    baseurl_scores = dataset["baseurl_scores"]
    files = dataset["files"]
    for f in files:
        annotation = f["annotation"]
        score = f["score"]
        url_annotation = os.path.join(baseurl_annotations, quote(annotation))
        localName = annotation.replace("/", "_")
        info = urlretrieve(url_annotation, f"{datasetFolder}/{datasetName}_{localName}")
        print(info[0])
        if baseurl_scores and score:
            url_score = os.path.join(baseurl_scores, quote(score))
            localName = score.replace("/", "_")
            info = urlretrieve(url_score, f"{datasetFolder}/{datasetName}_{localName}")
            print(info[0])
