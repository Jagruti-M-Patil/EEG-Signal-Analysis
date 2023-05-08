@REM Script to run analyst.py

@ECHO OFF

SET py_script="E:/Semester 2/IN 791/physionet.org/Codes/EEG-Signal-Analysis/analyst.py"
SET patient_id="chb01"

ECHO Invoking...

@REM chb01 training with ARMA
@REM -------------------------
@REM python %py_script% teach ^
@REM --patient=%patient_id% --method="ARMA" --learning_algorithm="Linear SVM" --data="./data" ^
@REM --learnersaveto="./models/%patient_id%/AR"

@REM python %py_script% teach ^
@REM --patient=%patient_id% --method="ARMA" --learning_algorithm="RBF SVM" --data="./data" ^
@REM --learnersaveto="./models/%patient_id%/AR"

@REM python %py_script% teach ^
@REM --patient=%patient_id% --method="ARMA" --learning_algorithm="Logistic Regression" --data="./data" ^
@REM --learnersaveto="./models/%patient_id%/AR" --plot_figures

@REM chb01 testing with ARMA
@REM -------------------------
@REM python %py_script% think ^
@REM --patient=%patient_id% --method="ARMA" --learner="chb01_ARMA_Linear_SVM_v2" --train ^
@REM --data="./data" --models="./models" --saveto="./figures/%patient_id%/AR" ^
@REM --saveformat=".jpeg"

@REM python %py_script% think ^
@REM --patient=%patient_id% --method="ARMA" --learner="chb01_ARMA_RBF_SVM_v2" --train ^
@REM --data="./data" --models="./models" --saveto="./figures/%patient_id%/AR" ^
@REM --saveformat=".jpeg"

@REM python %py_script% think ^
@REM --patient=%patient_id% --method="ARMA" --learner="chb01_ARMA_Logistic_Regression_v2" --train ^
@REM --data="./data" --models="./models" --saveto="./figures/%patient_id%/AR" ^
@REM --saveformat=".jpeg"
@REM --------------------

@REM chb01 prediction with ARMA (TEST set)
@REM -------------------------
python %py_script% think ^
--patient=%patient_id% --method="ARMA" --learner="chb01_ARMA_Linear_SVM_v2" ^
--data="./data" --models="./models" --saveto="./figures/%patient_id%/AR" ^
--saveformat=".jpeg"

@REM python %py_script% think ^
@REM --patient=%patient_id% --method="ARMA" --learner="chb01_ARMA_RBF_SVM_v2" ^
@REM --data="./data" --models="./models" --saveto="./figures/%patient_id%/AR" ^
@REM --saveformat=".jpeg" --prediction_only

@REM python %py_script% think ^
@REM --patient=%patient_id% --method="ARMA" --learner="chb01_ARMA_Logistic_Regression_v2" ^
@REM --data="./data" --models="./models" --saveto="./figures/%patient_id%/AR" ^
@REM --saveformat=".jpeg"
@REM -------------------------

@REM ------------------------- -------------------------  -------------------------

@REM chb01 training with Spectral Power in Band
@REM -------------------------------------------------- 
@REM python %py_script% teach ^
@REM --patient=%patient_id% --method="Spectral" --learning_algorithm="Linear SVM" --data="./data" ^
@REM --learnersaveto="./models/%patient_id%/Spectral"

@REM python %py_script% teach ^
@REM --patient=%patient_id% --method="Spectral" --learning_algorithm="RBF SVM" --data="./data" ^
@REM --learnersaveto="./models/%patient_id%/Spectral"

@REM python %py_script% teach ^
@REM --patient=%patient_id% --method="Spectral" --learning_algorithm="Logistic Regression" --data="./data" ^
@REM --learnersaveto="./models/%patient_id%/Spectral" --plot_figures

@REM chb01 testing with Spectral Power in Band
@REM -------------------------
@REM python %py_script% think ^
@REM --patient=%patient_id% --method="Spectral" --learner="chb01_Spectral_Linear_SVM_v2" --train ^
@REM --data="./data" --models="./models" --saveto="./figures/%patient_id%/Spectral" ^
@REM --saveformat=".jpeg" --kf

@REM python %py_script% think ^
@REM --patient=%patient_id% --method="Spectral" --learner="chb01_Spectral_RBF_SVM_v2" --train ^
@REM --data="./data" --models="./models" --saveto="./figures/%patient_id%/Spectral" ^
@REM --saveformat=".jpeg" --kf

@REM python %py_script% think ^
@REM --patient=%patient_id% --method="Spectral" --learner="chb01_Spectral_Logistic_Regression_v2" --train ^
@REM --data="./data" --models="./models" --saveto="./figures/%patient_id%/Spectral" ^
@REM --saveformat=".jpeg"
@REM -------------------------------------------------- 

@REM chb01 prediction with Spectral Power in Band (TEST set)
@REM -------------------------------------------------- 
@REM python %py_script% think ^
@REM --patient=%patient_id% --method="Spectral" --learner="chb01_Spectral_RBF_SVM_v2" ^
@REM --data="./data" --models="./models" --saveto="./figures/%patient_id%/Spectral" ^
@REM --saveformat=".jpeg" --prediction_only --kf

@REM -------------------------------------------------- 

