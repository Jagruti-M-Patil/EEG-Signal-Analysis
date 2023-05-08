@REM Script to run analyst.py

@ECHO OFF

SET py_script="/home/souritra/Documents/IN791/EEG-Signal-Analysis/analyst.py"
SET patient_id="chb01"

ECHO Invoking...

@REM chb01 training with ARMA
@REM -------------------------
python %py_script% teach \
--patient=%patient_id% --method='ARMA' --learning_algorithm='Linear SVM' --data='./data' \
--learnersaveto='./models/%patient_id%/AR/Linear-SVM/'

python %py_script% teach \
--patient=%patient_id% --method='ARMA' --learning_algorithm='RBF SVM' --data='./data' \
--learnersaveto='./models/%patient_id%/AR'

python %py_script% teach \
--patient=%patient_id% --method='ARMA' --learning_algorithm='Logistic Regression' --data='./data' \
--learnersaveto='./models/%patient_id%/AR' --plot_figures

@REM chb01 testing with ARMA
@REM -------------------------
python %py_script% think \
--patient=%patient_id% --method='ARMA' --learner='chb01_ARMA_Linear_SVM_v2' --train \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/AR' \
--saveformat='.jpeg'

python %py_script% think \
--patient=%patient_id% --method='ARMA' --learner='chb01_ARMA_RBF_SVM_v2' --train \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/AR' \
--saveformat='.jpeg'

python %py_script% think \
--patient=%patient_id% --method='ARMA' --learner='chb01_ARMA_Logistic_Regression_v2' --train \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/AR' \
--saveformat='.jpeg'
@REM --------------------

@REM chb01 prediction with ARMA (TEST set)
@REM -------------------------
python %py_script% think \
--patient=%patient_id% --method='ARMA' --learner='chb01_ARMA_Linear_SVM_v2' \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/AR' \
--saveformat='.jpeg'

python %py_script% think \
--patient=%patient_id% --method='ARMA' --learner='chb01_ARMA_RBF_SVM_v2' \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/AR' \
--saveformat='.jpeg' --prediction_only

python %py_script% think \
--patient=%patient_id% --method='ARMA' --learner='chb01_ARMA_Logistic_Regression_v2' \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/AR' \
--saveformat='.jpeg'
@REM -------------------------

@REM ------------------------- -------------------------  -------------------------

@REM chb01 training with Spectral Power in Band
@REM -------------------------------------------------- 
python %py_script% teach \
--patient=%patient_id% --method='Spectral' --learning_algorithm='Linear SVM' --data='./data' \
--learnersaveto='./models/%patient_id%/Spectral'

python %py_script% teach \
--patient=%patient_id% --method='Spectral' --learning_algorithm='RBF SVM' --data='./data' \
--learnersaveto='./models/%patient_id%/Spectral'

python %py_script% teach \
--patient=%patient_id% --method='Spectral' --learning_algorithm='Logistic Regression' --data='./data' \
--learnersaveto='./models/%patient_id%/Spectral' --plot_figures

@REM chb01 testing with Spectral Power in Band
@REM -------------------------
python %py_script% think \
--patient=%patient_id% --method='Spectral' --learner='chb01_Spectral_Linear_SVM_v2' --train \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/Spectral' \
--saveformat='.jpeg' --kf

python %py_script% think \
--patient=%patient_id% --method='Spectral' --learner='chb01_Spectral_RBF_SVM_v2' --train \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/Spectral' \
--saveformat='.jpeg' --kf

python %py_script% think \
--patient=%patient_id% --method='Spectral' --learner='chb01_Spectral_Logistic_Regression_v2' --train \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/Spectral' \
--saveformat='.jpeg'
@REM -------------------------------------------------- 

@REM chb01 prediction with Spectral Power in Band (TEST set)
@REM -------------------------------------------------- 
python %py_script% think \
--patient=%patient_id% --method='Spectral' --learner='chb01_Spectral_RBF_SVM_v2' \
--data='./data' --models='./models' --saveto='./figures/%patient_id%/Spectral' \
--saveformat='.jpeg' --prediction_only --kf

@REM -------------------------------------------------- 

