<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel - Analisis Gizi Makanan</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }
        
        .navbar {
            background: linear-gradient(135deg, #C62828 0%, #D32F2F 100%);
            color: white;
            padding: 20px 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .navbar h1 { font-size: 1.8em; }
        .navbar a { color: white; text-decoration: none; padding: 10px 20px; background: rgba(255,255,255,0.2); border-radius: 5px; transition: 0.3s; }
        .navbar a:hover { background: rgba(255,255,255,0.3); }
        
        .container { max-width: 1600px; margin: 30px auto; padding: 0 20px; }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .tab {
            padding: 15px 30px;
            background: white;
            border: none;
            border-radius: 10px 10px 0 0;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: 0.3s;
            color: #666;
        }
        
        .tab.active { background: #C62828; color: white; }
        .tab:hover { background: #E53935; color: white; }
        
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .panel {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .panel h2 {
            color: #C62828;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 3px solid #C62828;
            padding-bottom: 10px;
        }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        
        .stat-card {
            background: linear-gradient(135deg, #C62828 0%, #D32F2F 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stat-card h3 { font-size: 0.95em; opacity: 0.9; margin-bottom: 10px; }
        .stat-card .value { font-size: 2em; font-weight: bold; }
        
        .data-table-container {
            max-height: 400px;
            overflow: auto;
            border: 1px solid #ddd;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th {
            background: #C62828;
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #eee;
        }
        
        tr:hover { background: #f9f9f9; }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
        }
        
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #C62828;
        }
        
        .btn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #C62828 0%, #D32F2F 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
            margin-right: 10px;
        }
        
        .btn:hover {
            background: linear-gradient(135deg, #B71C1C 0%, #C62828 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #666 0%, #888 100%);
        }
        
        .btn-secondary:hover {
            background: linear-gradient(135deg, #555 0%, #777 100%);
        }
        
        .checkbox-group {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin: 15px 0;
        }
        
        .checkbox-group label {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }
        
        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .chart-container {
            margin: 20px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 10px;
        }
        
        .model-comparison {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .model-card {
            background: white;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            transition: 0.3s;
        }
        
        .model-card:hover {
            border-color: #C62828;
            box-shadow: 0 4px 12px rgba(198, 40, 40, 0.2);
        }
        
        .model-card h3 {
            color: #C62828;
            margin-bottom: 15px;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        
        .metric:last-child { border-bottom: none; }
        
        .metric-label { color: #666; }
        .metric-value { font-weight: bold; color: #333; }
        
        .alert {
            padding: 15px 20px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .alert-info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #f0f0f0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #C62828 0%, #D32F2F 100%);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>⚙️ Admin Panel - Analisis Gizi Makanan</h1>
        <a href="index.php">← Kembali ke Beranda</a>
    </div>
    
    <div class="container">
        <div class="tabs">
            <button class="tab active" onclick="showTab('preprocessing')">Data Preprocessing</button>
            <button class="tab" onclick="showTab('modeling')">Model Configuration</button>
            <button class="tab" onclick="showTab('visualization')">Data Visualization</button>
        </div>
        
        <!-- Tab 1: Data Preprocessing -->
        <div id="preprocessing" class="tab-content active">
            <div class="panel">
                <h2>📊 Dataset Preview</h2>
                <div id="datasetInfo" class="loading">Memuat data...</div>
                <div class="data-table-container">
                    <table id="dataTable">
                        <thead id="tableHeader"></thead>
                        <tbody id="tableBody"></tbody>
                    </table>
                </div>
            </div>
            
            <div class="panel">
                <h2>📈 Data Information</h2>
                <div class="grid">
                    <div class="stat-card">
                        <h3>Total Data</h3>
                        <div class="value" id="totalRows">-</div>
                    </div>
                    <div class="stat-card">
                        <h3>Total Kolom</h3>
                        <div class="value" id="totalCols">-</div>
                    </div>
                    <div class="stat-card">
                        <h3>Missing Values</h3>
                        <div class="value" id="missingValues">-</div>
                    </div>
                    <div class="stat-card">
                        <h3>Duplicate Rows</h3>
                        <div class="value" id="duplicateRows">-</div>
                    </div>
                </div>
                
                <h3 style="margin: 20px 0 10px 0; color: #C62828;">Tipe Data Kolom:</h3>
                <div id="dataTypes" class="data-table-container"></div>
                
                <h3 style="margin: 20px 0 10px 0; color: #C62828;">Statistik Deskriptif:</h3>
                <div id="descriptiveStats" class="data-table-container"></div>
            </div>
            
            <div class="panel">
                <h2>📉 Skewness Analysis</h2>
                <div id="skewnessAnalysis" class="data-table-container"></div>
            </div>
            
            <div class="panel">
                <h2>🧹 Data Cleaning Options</h2>
                <div class="checkbox-group">
                    <label><input type="checkbox" id="removeDuplicates"> Hapus Duplikat</label>
                    <label><input type="checkbox" id="handleMissing"> Tangani Missing Values</label>
                    <label><input type="checkbox" id="handleOutliers"> Tangani Outliers (IQR Method)</label>
                </div>
                <button class="btn" onclick="applyDataCleaning()">Terapkan Data Cleaning</button>
                <div id="cleaningResult"></div>
            </div>
            
            <div class="panel">
                <h2>🔄 Data Transformation</h2>
                <div class="form-group">
                    <label>Pilih Metode Transformasi:</label>
                    <select id="transformMethod">
                        <option value="standardize">Standardization (StandardScaler)</option>
                        <option value="normalize">Normalization (MinMaxScaler)</option>
                        <option value="robust">Robust Scaler</option>
                    </select>
                </div>
                <button class="btn" onclick="applyTransformation()">Terapkan Transformasi</button>
                <div id="transformResult"></div>
            </div>
        </div>
        
        <!-- Tab 2: Model Configuration -->
        <div id="modeling" class="tab-content">
            <div class="panel">
                <h2>🤖 Model Configuration</h2>
                <div class="grid">
                    <div class="form-group">
                        <label>Pilih Model:</label>
                        <select id="modelType" onchange="updateModelParams()">
                            <option value="random_forest">Random Forest</option>
                            <option value="naive_bayes">Naive Bayes</option>
                            <option value="svm">Support Vector Machine</option>
                            <option value="kmeans">K-Means Clustering</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Test Size (%):</label>
                        <input type="number" id="testSize" value="20" min="10" max="50">
                    </div>
                    
                    <div class="form-group">
                        <label>Random State:</label>
                        <input type="number" id="randomState" value="42" min="0">
                    </div>
                </div>
                
                <div id="modelSpecificParams"></div>
                
                <button class="btn" onclick="trainModel()">Latih Model</button>
                <button class="btn btn-secondary" onclick="trainAllModels()">Latih Semua Model</button>
                
                <div id="trainingProgress"></div>
                <div id="trainingResult"></div>
            </div>
            
            <div class="panel">
                <h2>📊 Model Comparison</h2>
                <div id="modelComparison" class="model-comparison"></div>
            </div>
        </div>
        
        <!-- Tab 3: Data Visualization -->
        <div id="visualization" class="tab-content">
            <div class="panel">
                <h2>📈 Data Distribution</h2>
                <div class="chart-container">
                    <canvas id="distributionChart"></canvas>
                </div>
            </div>
            
            <div class="panel">
                <h2>🎯 Correlation Heatmap</h2>
                <div class="chart-container">
                    <canvas id="correlationChart"></canvas>
                </div>
            </div>
            
            <div class="panel">
                <h2>📊 Feature Importance</h2>
                <div class="chart-container">
                    <canvas id="featureImportanceChart"></canvas>
                </div>
            </div>
            
            <div class="panel">
                <h2>🎨 Model Performance Visualization</h2>
                <div class="chart-container">
                    <canvas id="performanceChart"></canvas>
                </div>
            </div>
            
            <div class="panel">
                <h2>📉 Confusion Matrix</h2>
                <div class="chart-container">
                    <canvas id="confusionMatrixChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        let currentData = null;
        let trainedModels = {};
        
        // Tab switching
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // Initialize visualizations when switching to visualization tab
            if (tabName === 'visualization' && currentData) {
                initializeVisualizations();
            }
        }
        
        // Load initial data
        async function loadData() {
            try {
                const response = await fetch('admin_api.php?action=load_data');
                const data = await response.json();
                currentData = data;
                displayDataPreview(data);
                displayDataInfo(data);
                displayDataTypes(data);
                displayDescriptiveStats(data);
                displaySkewness(data);
            } catch (error) {
                document.getElementById('datasetInfo').innerHTML = '<div class="alert alert-error">Error loading data</div>';
            }
        }
        
        function displayDataPreview(data) {
            document.getElementById('datasetInfo').innerHTML = `<div class="alert alert-info">Dataset berisi ${data.rows.length} baris dan ${data.columns.length} kolom</div>`;
            
            const headerHtml = '<tr>' + data.columns.map(col => `<th>${col}</th>`).join('') + '</tr>';
            document.getElementById('tableHeader').innerHTML = headerHtml;
            
            const bodyHtml = data.preview.map(row => 
                '<tr>' + data.columns.map(col => `<td>${row[col] !== null ? row[col] : 'N/A'}</td>`).join('') + '</tr>'
            ).join('');
            document.getElementById('tableBody').innerHTML = bodyHtml;
        }
        
        function displayDataInfo(data) {
            document.getElementById('totalRows').textContent = data.rows.length;
            document.getElementById('totalCols').textContent = data.columns.length;
            document.getElementById('missingValues').textContent = data.missing_count || 0;
            document.getElementById('duplicateRows').textContent = data.duplicate_count || 0;
        }
        
        function displayDataTypes(data) {
            const html = '<table><thead><tr><th>Kolom</th><th>Tipe Data</th><th>Non-Null Count</th></tr></thead><tbody>' +
                data.dtypes.map(item => `<tr><td>${item.column}</td><td>${item.dtype}</td><td>${item.non_null}</td></tr>`).join('') +
                '</tbody></table>';
            document.getElementById('dataTypes').innerHTML = html;
        }
        
        function displayDescriptiveStats(data) {
            const stats = data.descriptive_stats;
            const columns = Object.keys(stats);
            const metrics = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'];
            
            let html = '<table><thead><tr><th>Metric</th>' + columns.map(col => `<th>${col}</th>`).join('') + '</tr></thead><tbody>';
            metrics.forEach(metric => {
                html += '<tr><td><strong>' + metric + '</strong></td>';
                columns.forEach(col => {
                    const value = stats[col][metric];
                    html += `<td>${value !== null && value !== undefined ? parseFloat(value).toFixed(2) : 'N/A'}</td>`;
                });
                html += '</tr>';
            });
            html += '</tbody></table>';
            document.getElementById('descriptiveStats').innerHTML = html;
        }
        
        function displaySkewness(data) {
            const html = '<table><thead><tr><th>Kolom</th><th>Skewness</th><th>Interpretation</th></tr></thead><tbody>' +
                data.skewness.map(item => {
                    let interpretation = 'Normal';
                    if (Math.abs(item.skewness) > 1) interpretation = 'Highly Skewed';
                    else if (Math.abs(item.skewness) > 0.5) interpretation = 'Moderately Skewed';
                    return `<tr><td>${item.column}</td><td>${item.skewness.toFixed(3)}</td><td>${interpretation}</td></tr>`;
                }).join('') +
                '</tbody></table>';
            document.getElementById('skewnessAnalysis').innerHTML = html;
        }
        
        async function applyDataCleaning() {
            const options = {
                remove_duplicates: document.getElementById('removeDuplicates').checked,
                handle_missing: document.getElementById('handleMissing').checked,
                handle_outliers: document.getElementById('handleOutliers').checked
            };
            
            document.getElementById('cleaningResult').innerHTML = '<div class="loading">Memproses...</div>';
            
            try {
                const response = await fetch('admin_api.php?action=clean_data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(options)
                });
                const result = await response.json();
                
                document.getElementById('cleaningResult').innerHTML = `
                    <div class="alert alert-success">
                        <strong>Data Cleaning Berhasil!</strong><br>
                        Baris sebelum: ${result.rows_before} → Baris setelah: ${result.rows_after}<br>
                        ${result.duplicates_removed > 0 ? `Duplikat dihapus: ${result.duplicates_removed}<br>` : ''}
                        ${result.outliers_removed > 0 ? `Outliers dihapus: ${result.outliers_removed}<br>` : ''}
                        ${result.missing_filled > 0 ? `Missing values diisi: ${result.missing_filled}` : ''}
                    </div>
                `;
                loadData(); // Reload data
            } catch (error) {
                document.getElementById('cleaningResult').innerHTML = '<div class="alert alert-error">Error: ' + error.message + '</div>';
            }
        }
        
        async function applyTransformation() {
            const method = document.getElementById('transformMethod').value;
            document.getElementById('transformResult').innerHTML = '<div class="loading">Memproses...</div>';
            
            try {
                const response = await fetch('admin_api.php?action=transform_data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({method})
                });
                const result = await response.json();
                
                document.getElementById('transformResult').innerHTML = `
                    <div class="alert alert-success">
                        <strong>Transformasi Berhasil!</strong><br>
                        Metode: ${result.method}<br>
                        Kolom yang ditransformasi: ${result.columns_transformed}
                    </div>
                `;
            } catch (error) {
                document.getElementById('transformResult').innerHTML = '<div class="alert alert-error">Error: ' + error.message + '</div>';
            }
        }
        
        function updateModelParams() {
            const modelType = document.getElementById('modelType').value;
            let html = '';
            
            if (modelType === 'random_forest') {
                html = `
                    <div class="grid">
                        <div class="form-group"><label>N Estimators:</label><input type="number" id="n_estimators" value="100" min="10"></div>
                        <div class="form-group"><label>Max Depth:</label><input type="number" id="max_depth" value="10" min="1"></div>
                    </div>
                `;
            } else if (modelType === 'svm') {
                html = `
                    <div class="grid">
                        <div class="form-group"><label>Kernel:</label><select id="kernel"><option>rbf</option><option>linear</option><option>poly</option></select></div>
                        <div class="form-group"><label>C:</label><input type="number" id="c_param" value="1.0" step="0.1"></div>
                    </div>
                `;
            } else if (modelType === 'kmeans') {
                html = `
                    <div class="grid">
                        <div class="form-group"><label>Number of Clusters:</label><input type="number" id="n_clusters" value="4" min="2"></div>
                        <div class="form-group"><label>Max Iterations:</label><input type="number" id="max_iter" value="300" min="100"></div>
                    </div>
                `;
            }
            
            document.getElementById('modelSpecificParams').innerHTML = html;
        }
        
        async function trainModel() {
            const modelType = document.getElementById('modelType').value;
            
            document.getElementById('trainingProgress').innerHTML = `
                <div class="progress-bar"><div class="progress-fill" style="width: 50%">Training ${modelType}...</div></div>
            `;
            
            try {
                const result = await trainSingleModel(modelType, true);
                
                document.getElementById('trainingProgress').innerHTML = `
                    <div class="progress-bar"><div class="progress-fill" style="width: 100%">Complete!</div></div>
                `;
                
                document.getElementById('trainingResult').innerHTML = `
                    <div class="alert alert-success">
                        <strong>Model ${result.model_name} Berhasil Dilatih!</strong><br>
                        Accuracy: ${result.accuracy}%<br>
                        ${result.precision ? `Precision: ${result.precision}%<br>` : ''}
                        ${result.recall ? `Recall: ${result.recall}%<br>` : ''}
                        ${result.f1_score ? `F1-Score: ${result.f1_score}%` : ''}
                    </div>
                `;
                
                updateVisualization(result);
            } catch (error) {
                document.getElementById('trainingProgress').innerHTML = '';
                document.getElementById('trainingResult').innerHTML = '<div class="alert alert-error">Error: ' + error.message + '</div>';
            }
        }
        
        async function trainAllModels() {
            const models = ['random_forest', 'naive_bayes', 'svm', 'kmeans'];
            const originalModel = document.getElementById('modelType').value;
            
            // Clear previous results
            trainedModels = {};
            document.getElementById('trainingProgress').innerHTML = '<div class="loading">Melatih semua model...</div>';
            document.getElementById('trainingResult').innerHTML = '';
            document.getElementById('modelComparison').innerHTML = '<div class="loading">Training in progress...</div>';
            
            let successCount = 0;
            
            for (let i = 0; i < models.length; i++) {
                const model = models[i];
                document.getElementById('modelType').value = model;
                updateModelParams();
                
                document.getElementById('trainingProgress').innerHTML = `
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${((i + 0.5) / models.length) * 100}%">
                            Training ${i + 1}/${models.length}: ${model}
                        </div>
                    </div>
                `;
                
                try {
                    const result = await trainSingleModel(model);
                    console.log(`Trained ${model}:`, result);
                    successCount++;
                    
                    // Update progress after each model
                    document.getElementById('trainingProgress').innerHTML = `
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${((i + 1) / models.length) * 100}%">
                                Completed ${i + 1}/${models.length}: ${result.model_name}
                            </div>
                        </div>
                    `;
                } catch (error) {
                    console.error(`Error training ${model}:`, error);
                }
                
                await new Promise(resolve => setTimeout(resolve, 800));
            }
            
            document.getElementById('modelType').value = originalModel;
            updateModelParams();
            
            // Final update of comparison
            updateModelComparison();
            
            document.getElementById('trainingProgress').innerHTML = `
                <div class="alert alert-success">
                    <strong>Training Selesai!</strong><br>
                    ${successCount} dari ${models.length} model berhasil dilatih.<br>
                    Models trained: ${Object.keys(trainedModels).join(', ')}
                </div>
            `;
        }
        
        async function trainSingleModel(modelType, updateComparison = false) {
            const testSize = document.getElementById('testSize').value / 100;
            const randomState = document.getElementById('randomState').value;
            
            const params = {
                model_type: modelType,
                test_size: testSize,
                random_state: randomState
            };
            
            // Add model-specific params with defaults
            if (modelType === 'random_forest') {
                const nEstimators = document.getElementById('n_estimators');
                const maxDepth = document.getElementById('max_depth');
                params.n_estimators = nEstimators ? parseInt(nEstimators.value) : 100;
                params.max_depth = maxDepth ? parseInt(maxDepth.value) : 10;
            } else if (modelType === 'svm') {
                const kernel = document.getElementById('kernel');
                const cParam = document.getElementById('c_param');
                params.kernel = kernel ? kernel.value : 'rbf';
                params.C = cParam ? parseFloat(cParam.value) : 1.0;
            } else if (modelType === 'kmeans') {
                const nClusters = document.getElementById('n_clusters');
                const maxIter = document.getElementById('max_iter');
                params.n_clusters = nClusters ? parseInt(nClusters.value) : 4;
                params.max_iter = maxIter ? parseInt(maxIter.value) : 300;
            }
            
            console.log(`Training ${modelType} with params:`, params);
            
            const response = await fetch('admin_api.php?action=train_model', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(params)
            });
            
            const result = await response.json();
            
            if (result.error) {
                console.error(`Error response for ${modelType}:`, result);
                throw new Error(result.error);
            }
            
            // Store with unique key
            trainedModels[modelType] = result;
            console.log(`Successfully stored ${modelType}: ${result.model_name}`);
            console.log('All trained models so far:', Object.keys(trainedModels).map(k => `${k}=${trainedModels[k].model_name}`));
            
            if (updateComparison) {
                updateModelComparison();
            }
            
            return result;
        }
        
        function updateModelComparison() {
            let html = '';
            Object.keys(trainedModels).forEach(modelType => {
                const model = trainedModels[modelType];
                html += `
                    <div class="model-card">
                        <h3>${model.model_name}</h3>
                        <div class="metric"><span class="metric-label">Accuracy</span><span class="metric-value">${model.accuracy}%</span></div>
                        ${model.precision ? `<div class="metric"><span class="metric-label">Precision</span><span class="metric-value">${model.precision}%</span></div>` : ''}
                        ${model.recall ? `<div class="metric"><span class="metric-label">Recall</span><span class="metric-value">${model.recall}%</span></div>` : ''}
                        ${model.f1_score ? `<div class="metric"><span class="metric-label">F1-Score</span><span class="metric-value">${model.f1_score}%</span></div>` : ''}
                        <div class="metric"><span class="metric-label">Training Time</span><span class="metric-value">${model.training_time}s</span></div>
                    </div>
                `;
            });
            document.getElementById('modelComparison').innerHTML = html || '<div class="alert alert-info">Belum ada model yang dilatih</div>';
        }
        
        function updateVisualization(result) {
            // Update charts with model results
            if (result.feature_importance) {
                createFeatureImportanceChart(result.feature_importance);
            }
            if (result.confusion_matrix) {
                createConfusionMatrixChart(result.confusion_matrix);
            }
            // Update performance chart with all trained models
            if (Object.keys(trainedModels).length > 0) {
                createPerformanceChart();
            }
        }
        
        let featureChart = null;
        let confusionChart = null;
        let distributionChart = null;
        let correlationChart = null;
        let performanceChart = null;
        
        function initializeVisualizations() {
            if (!currentData) return;
            
            // Create distribution chart
            createDistributionChart();
            
            // Create correlation chart (simple version without actual correlation calculation)
            createCorrelationChart();
            
            // Show placeholder for model-dependent charts
            if (Object.keys(trainedModels).length > 0) {
                createPerformanceChart();
                const firstModel = trainedModels[Object.keys(trainedModels)[0]];
                if (firstModel.feature_importance) {
                    createFeatureImportanceChart(firstModel.feature_importance);
                }
                if (firstModel.confusion_matrix) {
                    createConfusionMatrixChart(firstModel.confusion_matrix);
                }
            }
        }
        
        function createDistributionChart() {
            const canvas = document.getElementById('distributionChart');
            const ctx = canvas.getContext('2d');
            
            if (distributionChart) {
                distributionChart.destroy();
            }
            
            // Create a simple bar chart showing label distribution
            const labelCounts = {};
            currentData.rows.forEach(row => {
                const label = row.label || 'Unknown';
                labelCounts[label] = (labelCounts[label] || 0) + 1;
            });
            
            distributionChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(labelCounts),
                    datasets: [{
                        label: 'Jumlah Data per Label',
                        data: Object.values(labelCounts),
                        backgroundColor: ['#4CAF50', '#8BC34A', '#FF9800', '#F44336']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
        
        function createCorrelationChart() {
            const canvas = document.getElementById('correlationChart');
            const ctx = canvas.getContext('2d');
            
            if (correlationChart) {
                correlationChart.destroy();
            }
            
            // Simple representation showing feature relationships
            const features = ['calories', 'proteins', 'fat', 'carbohydrate'];
            
            correlationChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: features,
                    datasets: [{
                        label: 'Mean Values',
                        data: features.map(f => {
                            const stats = currentData.descriptive_stats[f];
                            return stats ? parseFloat(stats.mean) : 0;
                        }),
                        backgroundColor: '#C62828'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
        
        function createPerformanceChart() {
            const canvas = document.getElementById('performanceChart');
            const ctx = canvas.getContext('2d');
            
            if (performanceChart) {
                performanceChart.destroy();
            }
            
            const modelNames = Object.keys(trainedModels).map(k => trainedModels[k].model_name);
            const accuracies = Object.keys(trainedModels).map(k => trainedModels[k].accuracy);
            
            performanceChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: modelNames,
                    datasets: [{
                        label: 'Accuracy (%)',
                        data: accuracies,
                        backgroundColor: '#C62828'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: { 
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
        
        function createFeatureImportanceChart(data) {
            const canvas = document.getElementById('featureImportanceChart');
            const ctx = canvas.getContext('2d');
            
            // Destroy existing chart if it exists
            if (featureChart) {
                featureChart.destroy();
            }
            
            featureChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.features,
                    datasets: [{
                        label: 'Feature Importance',
                        data: data.importance,
                        backgroundColor: '#C62828'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
        
        function createConfusionMatrixChart(matrix) {
            const canvas = document.getElementById('confusionMatrixChart');
            const ctx = canvas.getContext('2d');
            
            // Destroy existing chart if it exists
            if (confusionChart) {
                confusionChart.destroy();
            }
            
            // Flatten the confusion matrix for heatmap-like visualization
            const labels = ['Sangat Baik', 'Baik', 'Buruk', 'Sangat Buruk'];
            confusionChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: labels.map((label, idx) => ({
                        label: `Predicted: ${label}`,
                        data: matrix[idx] || [],
                        backgroundColor: `rgba(198, 40, 40, ${0.3 + idx * 0.15})`
                    }))
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
        
        // Initialize
        loadData();
        updateModelParams();
    </script>
</body>
</html>
