' Excel VBA macro — assign this to your button (Step 3)
' Update PYTHON_PATH and SCRIPT_PATH to match your machine.

Sub RunSupplyChainPipeline()
    Dim pythonPath As String
    Dim scriptPath As String
    Dim cmd As String
    Dim exitCode As Integer

    ThisWorkbook.Save

    pythonPath = "/usr/local/bin/python3"
    scriptPath = "/Users/aryal/Documents/Projects/Supply-Chain-Analysis-/step3/excel/run_pipeline.py"

    cmd = pythonPath & " " & Chr(34) & scriptPath & Chr(34)
    exitCode = Shell(cmd, vbNormalFocus)

    If exitCode = 0 Then
        MsgBox "Pipeline started. Check terminal / S3 for output.", vbInformation
    Else
        MsgBox "Could not start Python. Update paths in RunPipeline.bas", vbExclamation
    End If
End Sub
