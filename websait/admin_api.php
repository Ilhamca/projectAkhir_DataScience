<?php
header('Content-Type: application/json');
error_reporting(E_ALL);
ini_set('display_errors', 0);

$action = $_GET['action'] ?? '';

try {
    switch ($action) {
        case 'load_data':
            loadData();
            break;
        case 'clean_data':
            cleanData();
            break;
        case 'transform_data':
            transformData();
            break;
        case 'train_model':
            trainModel();
            break;
        default:
            echo json_encode(['error' => 'Invalid action']);
    }
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}

function loadData() {
    $output = shell_exec('C:/Users/RAFFY/anaconda3/python.exe admin_operations.py load_data 2>&1');
    echo $output;
}

function cleanData() {
    $input = json_decode(file_get_contents('php://input'), true);
    $options = json_encode($input, JSON_UNESCAPED_SLASHES);
    $tempFile = tempnam(sys_get_temp_dir(), 'clean_');
    file_put_contents($tempFile, $options);
    $output = shell_exec("C:/Users/RAFFY/anaconda3/python.exe admin_operations.py clean_data_file \"$tempFile\" 2>&1");
    unlink($tempFile);
    echo $output;
}

function transformData() {
    $input = json_decode(file_get_contents('php://input'), true);
    $method = $input['method'] ?? 'standardize';
    $output = shell_exec("C:/Users/RAFFY/anaconda3/python.exe admin_operations.py transform_data $method 2>&1");
    echo $output;
}

function trainModel() {
    $input = json_decode(file_get_contents('php://input'), true);
    $params = json_encode($input, JSON_UNESCAPED_SLASHES);
    $tempFile = tempnam(sys_get_temp_dir(), 'train_');
    file_put_contents($tempFile, $params);
    $output = shell_exec("C:/Users/RAFFY/anaconda3/python.exe admin_operations.py train_model_file \"$tempFile\" 2>&1");
    unlink($tempFile);
    echo $output;
}
?>
