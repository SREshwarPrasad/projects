
<h2>Paddy Disease Classification using ML and DL Techniques </h2>

<h3> About: </h3>

This project focuses on Paddy Leaf Disease Classification using both Deep Learning 
and Machine Learning techniques. The dataset consists of multiple disease categories 
such as bacterial leaf blight, brown spot, blast, tungro, hispa, and more. Each folder 
contains image samples of the corresponding disease type. All algorithms are trained on 450 images per disease.  

<h3> Algorithms: </h3>   

i) SVM+PCA (svmPca.ipynb)
ii) CNN (cnn.ipynb)
iii) KLDA (klda.ipynb)
iv) Random Forest (rf.ipynb)

<h3>Folder Structure:</h3>

    paddydisease/
        |
        ├── bacterial_leaf_blight/
        ├── bacterial_leaf_streak/
        ├── bacterial_panicile_blight/
        ├── balanced/
        ├── black_stem_borer/
        ├── blast/
        ├── brown_spot/
        ├── downy_mildew/
        ├── hispa/
        ├── leaf_roller/
        ├── normal/
        ├── output_cascade_rcnn/
        ├── tungro/
        ├── white_stem_borer/
        ├── yellow_stem_borer/
        ├── balanced_coco/        # JSON export (COCO format)
        └── metadata.xlsx  
<h3> Result: </h3>    
<table>
    <tr>
        <td align="center"> <b> MODEL </b> </td>
        <td align="center"> <b> ACCURACY </b> </td>
    </tr>
    <tr>
        <td align="center"> SVM+PCA </td>
        <td align="center">  75.00% </td>
    </tr>
    <tr>
        <td align="center"> CNN </td>
        <td align="center"> 74.19% </td>
    </tr>
    <tr>
        <td align="center"> KLDA </td>
        <td align="center"> 98.12% </td>
    </tr>
    <tr>
        <td align="center"> Random Forest </td>
        <td align="center"> 82.74% </td>
    </tr>
</table>  

<h3> Dataset: </h3> https://drive.google.com/file/d/1xveT_m8JmJb-4vA825yD80XnoyoRL_iM/view?usp=drive_link
