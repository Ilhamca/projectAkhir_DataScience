<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analisis Gizi Makanan Indonesia</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 50%, #A5D6A7 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container { max-width: 1400px; margin: 0 auto; }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            position: relative;
        }
        
        .back-btn {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            transition: 0.3s;
        }
        
        .back-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        
        header h1 { font-size: 2.8em; margin-bottom: 10px; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); }
        header p { font-size: 1.2em; opacity: 0.95; }
        
        .search-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .search-input {
            width: 100%;
            padding: 15px;
            border: 3px solid #388E3C;
            border-radius: 10px;
            font-size: 1.1em;
            margin-bottom: 15px;
        }
        
        .search-input:focus { outline: none; border-color: #1B5E20; box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1); }
        
        .model-selector {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .model-selector label {
            font-weight: 600;
            color: #2E7D32;
            min-width: 150px;
        }
        
        .model-selector select {
            flex: 1;
            padding: 12px;
            border: 2px solid #388E3C;
            border-radius: 8px;
            font-size: 1em;
            background: white;
            cursor: pointer;
        }
        
        .food-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .food-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            transition: all 0.3s;
            cursor: pointer;
            border: 3px solid transparent;
        }
        
        .food-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
            border-color: #388E3C;
        }
        
        .food-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            background: #f5f5f5;
        }
        
        .food-info { padding: 15px; }
        
        .food-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #2E7D32;
            margin-bottom: 10px;
        }
        
        .food-nutrition {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 8px;
        }
        
        .food-label {
            display: inline-block;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-top: 10px;
        }
        
        .label-sangat-baik { background: #4CAF50; color: white; }
        .label-baik { background: #8BC34A; color: white; }
        .label-buruk { background: #FF9800; color: white; }
        .label-sangat-buruk { background: #F44336; color: white; }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            overflow-y: auto;
        }
        
        .modal-content {
            background: white;
            max-width: 900px;
            margin: 50px auto;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        
        .modal-header {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
            color: white;
            padding: 25px;
            position: relative;
        }
        
        .modal-close {
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 2em;
            cursor: pointer;
            color: white;
            background: none;
            border: none;
        }
        
        .modal-body { padding: 30px; }
        
        .modal-image {
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        
        .nutrition-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .nutrition-item {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #388E3C;
        }
        
        .nutrition-label { font-size: 0.9em; color: #666; margin-bottom: 5px; }
        .nutrition-value { font-size: 1.3em; font-weight: bold; color: #2E7D32; }
        
        .btn-analyze {
            background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            width: 100%;
            transition: all 0.3s;
        }
        
        .btn-analyze:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(46, 125, 50, 0.4);
        }
        
        .result-box {
            margin-top: 20px;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }
        
        .result-box.show { display: block; }
        .loading { text-align: center; padding: 40px; color: #666; }
        .no-results { text-align: center; padding: 40px; color: #999; font-size: 1.2em; }
        
        /* Color-coded quality badges for food recommendations */
        .quality-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        .quality-sangat-baik {
            background: #4CAF50;
            color: white;
        }
        
        .quality-baik {
            background: #8BC34A;
            color: white;
        }
        
        .quality-buruk {
            background: #FF9800;
            color: white;
        }
        
        .quality-sangat-buruk {
            background: #F44336;
            color: white;
        }
        
        @media (max-width: 768px) {
            .food-grid { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
            .nutrition-grid { grid-template-columns: 1fr; }
            header h1 { font-size: 2em; }
            .back-btn { position: relative; left: 0; transform: none; display: block; margin-bottom: 15px; text-align: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <a href="index.php" class="back-btn">← Kembali</a>
            <h1>🥗 Sistem Rekomendasi Makanan Sehat</h1>
            <p>Dapatkan rekomendasi makanan personal berdasarkan kebutuhan nutrisi Anda</p>
        </header>

        <div class="search-section">
            <h3 style="color: #2E7D32; margin-bottom: 15px;">🎯 Pilih Tujuan Diet Anda</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px;">
                <button onclick="setDietGoal('weight-loss')" style="padding: 12px; background: white; border: 2px solid #388E3C; border-radius: 8px; cursor: pointer; font-weight: 600; transition: 0.3s;">🏃 Turun Berat</button>
                <button onclick="setDietGoal('muscle-gain')" style="padding: 12px; background: white; border: 2px solid #388E3C; border-radius: 8px; cursor: pointer; font-weight: 600; transition: 0.3s;">💪 Nambah Otot</button>
                <button onclick="setDietGoal('healthy')" style="padding: 12px; background: white; border: 2px solid #388E3C; border-radius: 8px; cursor: pointer; font-weight: 600; transition: 0.3s;">🥗 Sehat Seimbang</button>
                <button onclick="setDietGoal('low-calorie')" style="padding: 12px; background: white; border: 2px solid #388E3C; border-radius: 8px; cursor: pointer; font-weight: 600; transition: 0.3s;">🔥 Rendah Kalori</button>
            </div>

            <h4 style="color: #2E7D32; margin: 20px 0 10px 0;">📊 Kriteria Detail (atau gunakan preset di atas)</h4>
            <div class="criteria-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px;">
                <div>
                    <label style="display: block; margin-bottom: 5px; font-weight: 600;">Target Kalori (max):</label>
                    <input type="number" id="maxCalories" value="300" min="0" style="width: 100%; padding: 10px; border: 2px solid #388E3C; border-radius: 5px;">
                </div>
                <div>
                    <label style="display: block; margin-bottom: 5px; font-weight: 600;">Protein Minimum (g):</label>
                    <input type="number" id="minProtein" value="10" min="0" style="width: 100%; padding: 10px; border: 2px solid #388E3C; border-radius: 5px;">
                </div>
                <div>
                    <label style="display: block; margin-bottom: 5px; font-weight: 600;">Kualitas Minimum:</label>
                    <select id="minQuality" style="width: 100%; padding: 10px; border: 2px solid #388E3C; border-radius: 5px;">
                        <option value="Sangat Baik">Hanya Sangat Baik</option>
                        <option value="Baik" selected>Baik atau Lebih</option>
                        <option value="Buruk">Buruk atau Lebih</option>
                        <option value="Sangat Buruk">Semua Makanan</option>
                    </select>
                </div>
            </div>
            <button onclick="getRecommendations()" style="width: 100%; padding: 15px; background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%); color: white; border: none; border-radius: 10px; font-size: 1.1em; font-weight: bold; cursor: pointer; margin-bottom: 15px;">🔍 Dapatkan Rekomendasi</button>
            <div id="recommendationSummary" style="display: none; padding: 15px; background: #E8F5E9; border-left: 4px solid #4CAF50; border-radius: 5px; margin-bottom: 15px;"></div>
        </div>

        <div class="search-section">
            <h3 style="color: #2E7D32; margin-bottom: 10px;">🔎 Cari Makanan Spesifik (Opsional)</h3>
            <input type="text" id="searchInput" class="search-input" 
                   placeholder="Cari dari hasil rekomendasi... (contoh: ayam, tahu, tempe)" autocomplete="off">
            
            <div class="model-selector">
                <label for="modelSelect">🤖 Pilih Model Machine Learning:</label>
                <select id="modelSelect">
                    <option value="random_forest">Random Forest (92.59% Akurasi) ⭐</option>
                    <option value="naive_bayes">Naive Bayes</option>
                    <option value="kmeans">K-Means Clustering</option>
                    <option value="svm">SVM (Support Vector Machine)</option>
                </select>
            </div>
            <div style="padding: 10px; background: #E3F2FD; border-radius: 5px; margin-top: 10px; font-size: 0.9em;">
                💡 <strong>Semua makanan telah diklasifikasi menggunakan model ML yang dilatih di Jupyter Notebook</strong><br>
                Ganti model untuk melihat prediksi berbeda berdasarkan algoritma yang dipilih
            </div>
        </div>

        <div id="foodGrid" class="food-grid">
            <div class="loading">Memuat data makanan...</div>
        </div>
    </div>

    <div id="foodModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <button class="modal-close" onclick="closeModal()">&times;</button>
                <h2 id="modalTitle">Detail Makanan</h2>
            </div>
            <div class="modal-body">
                <img id="modalImage" class="modal-image" src="" alt="">
                <div id="modalInfo"></div>
            </div>
        </div>
    </div>

    <script>
        let foodsData = [];
        let recommendedFoods = [];
        let selectedModel = 'random_forest';

        // Quality ranking for filtering
        const qualityRank = {
            'Sangat Baik': 4,
            'Baik': 3,
            'Buruk': 2,
            'Sangat Buruk': 1
        };

        // Diet goal presets based on common nutrition recommendations
        function setDietGoal(goal) {
            switch(goal) {
                case 'weight-loss':
                    document.getElementById('maxCalories').value = 200;
                    document.getElementById('minProtein').value = 15;
                    document.getElementById('minQuality').value = 'Baik';
                    break;
                case 'muscle-gain':
                    document.getElementById('maxCalories').value = 400;
                    document.getElementById('minProtein').value = 25;
                    document.getElementById('minQuality').value = 'Baik';
                    break;
                case 'healthy':
                    document.getElementById('maxCalories').value = 300;
                    document.getElementById('minProtein').value = 10;
                    document.getElementById('minQuality').value = 'Sangat Baik';
                    break;
                case 'low-calorie':
                    document.getElementById('maxCalories').value = 150;
                    document.getElementById('minProtein').value = 5;
                    document.getElementById('minQuality').value = 'Baik';
                    break;
            }
            getRecommendations();
        }

        function getRecommendations() {
            const maxCalories = parseFloat(document.getElementById('maxCalories').value);
            const minProtein = parseFloat(document.getElementById('minProtein').value);
            const minQuality = document.getElementById('minQuality').value;
            const minQualityRank = qualityRank[minQuality];

            // Filter foods based on criteria
            recommendedFoods = foodsData.filter(food => {
                const calories = parseFloat(food.calories);
                const protein = parseFloat(food.proteins);
                const foodQualityRank = qualityRank[food.label] || 0;

                return calories <= maxCalories && 
                       protein >= minProtein && 
                       foodQualityRank >= minQualityRank;
            });

            // Sort by quality (best first), then by protein (highest first)
            recommendedFoods.sort((a, b) => {
                const qualityDiff = qualityRank[b.label] - qualityRank[a.label];
                if (qualityDiff !== 0) return qualityDiff;
                return parseFloat(b.proteins) - parseFloat(a.proteins);
            });

            // Display summary
            const summary = document.getElementById('recommendationSummary');
            if (recommendedFoods.length > 0) {
                const avgCalories = (recommendedFoods.reduce((sum, f) => sum + parseFloat(f.calories), 0) / recommendedFoods.length).toFixed(1);
                const avgProtein = (recommendedFoods.reduce((sum, f) => sum + parseFloat(f.proteins), 0) / recommendedFoods.length).toFixed(1);
                const sangatBaik = recommendedFoods.filter(f => f.label === 'Sangat Baik').length;
                const baik = recommendedFoods.filter(f => f.label === 'Baik').length;
                
                summary.innerHTML = `
                    <strong>✅ Ditemukan ${recommendedFoods.length} makanan yang sesuai!</strong><br>
                    📊 Rata-rata: ${avgCalories} kcal, ${avgProtein}g protein<br>
                    🌟 Kualitas: ${sangatBaik} Sangat Baik, ${baik} Baik
                `;
                summary.style.display = 'block';
            } else {
                summary.innerHTML = '<strong>❌ Tidak ada makanan yang memenuhi kriteria.</strong><br>Coba sesuaikan kriteria Anda.';
                summary.style.background = '#FFEBEE';
                summary.style.borderColor = '#F44336';
                summary.style.display = 'block';
            }

            // Display recommended foods
            displayFoods(recommendedFoods);
        }

        // Load foods with selected model predictions
        function loadFoodsWithModel(model) {
            document.getElementById('foodGrid').innerHTML = '<div class="loading">Memuat data dengan model ' + getModelName(model) + '...</div>';
            
            fetch('get_foods.php?model=' + model)
                .then(response => response.json())
                .then(data => {
                    foodsData = data;
                    recommendedFoods = []; // Reset recommendations when changing model
                    displayFoods(data);
                    
                    // Show model info
                    if (data.length > 0 && data[0].model_used) {
                        console.log('Loaded ' + data.length + ' foods classified by ' + data[0].model_used + ' model');
                    }
                })
                .catch(error => {
                    document.getElementById('foodGrid').innerHTML = '<div class="no-results">❌ Gagal memuat data makanan</div>';
                    console.error('Error loading foods:', error);
                });
        }

        // Initial load with default model
        loadFoodsWithModel(selectedModel);

        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            // Search from recommended foods if available, otherwise all foods
            const searchPool = recommendedFoods.length > 0 ? recommendedFoods : foodsData;
            const filtered = searchPool.filter(food => food.name.toLowerCase().includes(searchTerm));
            displayFoods(filtered);
        });

        document.getElementById('modelSelect').addEventListener('change', function(e) {
            selectedModel = e.target.value;
            // Reload data with new model
            loadFoodsWithModel(selectedModel);
        });

        function displayFoods(foods) {
            const grid = document.getElementById('foodGrid');
            if (foods.length === 0) {
                grid.innerHTML = '<div class="no-results">Tidak ada makanan yang ditemukan</div>';
                return;
            }

            grid.innerHTML = foods.map(food => `
                <div class="food-card" onclick="showFoodDetail(${food.id})">
                    <img src="${food.image}" alt="${food.name}" class="food-image"
                         onerror="this.src='https://via.placeholder.com/280x200?text=${encodeURIComponent(food.name)}'">
                    <div class="food-info">
                        <div class="food-name">${food.name}</div>
                        <div class="food-nutrition"><strong>Kalori:</strong> ${parseFloat(food.calories).toFixed(1)} kcal</div>
                        <div class="food-nutrition"><strong>Protein:</strong> ${parseFloat(food.proteins).toFixed(1)}g | <strong>Lemak:</strong> ${parseFloat(food.fat).toFixed(1)}g</div>
                        <div class="food-nutrition"><strong>Karbohidrat:</strong> ${parseFloat(food.carbohydrate).toFixed(1)}g</div>
                        <span class="food-label ${getLabelClass(food.label)}">${food.label}</span>
                        ${food.confidence ? `<div style="font-size: 0.85em; color: #666; margin-top: 5px;">🤖 AI: ${food.confidence.toFixed(1)}% yakin</div>` : ''}
                    </div>
                </div>
            `).join('');
        }

        function getLabelClass(label) {
            const map = {'Sangat Baik': 'label-sangat-baik', 'Baik': 'label-baik', 'Buruk': 'label-buruk', 'Sangat Buruk': 'label-sangat-buruk'};
            return map[label] || 'label-buruk';
        }

        function getQualityClass(label) {
            const map = {'Sangat Baik': 'quality-sangat-baik', 'Baik': 'quality-baik', 'Buruk': 'quality-buruk', 'Sangat Buruk': 'quality-sangat-buruk'};
            return map[label] || 'quality-buruk';
        }

        function showFoodDetail(foodId) {
            const food = foodsData.find(f => f.id == foodId);
            if (!food) return;

            document.getElementById('modalTitle').textContent = food.name;
            document.getElementById('modalImage').src = food.image;
            
            // Generate recommendation reason
            const proteinRatio = (parseFloat(food.proteins) / (parseFloat(food.calories) + 0.001) * 100).toFixed(1);
            let reason = '';
            if (food.label === 'Sangat Baik') {
                reason = '🌟 Makanan ini memiliki profil nutrisi sangat baik dengan keseimbangan kalori dan makronutrien yang optimal.';
            } else if (food.label === 'Baik') {
                reason = '✅ Makanan ini cocok untuk diet sehat dengan nutrisi yang cukup seimbang.';
            } else if (food.label === 'Buruk') {
                reason = '⚠️ Konsumsi dalam porsi terbatas. Pertimbangkan alternatif yang lebih sehat.';
            } else {
                reason = '❌ Tidak direkomendasikan untuk konsumsi rutin. Cari alternatif yang lebih baik.';
            }

            const confidenceText = food.confidence ? `<br><small>🎯 Confidence Score: ${food.confidence.toFixed(1)}%</small>` : '';
            const modelInfo = food.model_used ? `<br><small>📊 Diklasifikasi menggunakan model: <strong>${getModelName(food.model_used)}</strong></small>` : '';
            
            document.getElementById('modalInfo').innerHTML = `
                <div style="padding: 15px; background: ${food.label === 'Sangat Baik' ? '#E8F5E9' : food.label === 'Baik' ? '#F1F8E9' : food.label === 'Buruk' ? '#FFF3E0' : '#FFEBEE'}; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid ${food.label === 'Sangat Baik' ? '#4CAF50' : food.label === 'Baik' ? '#8BC34A' : food.label === 'Buruk' ? '#FF9800' : '#F44336'};">
                    <strong>🤖 Prediksi Model ML:</strong> ${reason}<br>
                    <small>Rasio Protein: ${proteinRatio}% dari kalori</small>
                    ${confidenceText}
                    ${modelInfo}
                </div>
                
                <h3 style="color: #2E7D32; margin-bottom: 15px;">Informasi Gizi</h3>
                <div class="nutrition-grid">
                    <div class="nutrition-item"><div class="nutrition-label">Kalori</div><div class="nutrition-value">${parseFloat(food.calories).toFixed(1)} kcal</div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Protein</div><div class="nutrition-value">${parseFloat(food.proteins).toFixed(1)} g</div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Lemak</div><div class="nutrition-value">${parseFloat(food.fat).toFixed(1)} g</div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Karbohidrat</div><div class="nutrition-value">${parseFloat(food.carbohydrate).toFixed(1)} g</div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Prediksi AI</div><div class="nutrition-value"><span class="quality-badge ${getQualityClass(food.label)}">${food.label}</span></div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Model Aktif</div><div class="nutrition-value" style="font-size: 1em;">${getModelName(selectedModel)}</div></div>
                </div>
                ${food.original_label && food.original_label !== food.label ? `<div style="padding: 10px; background: #FFF9C4; border-radius: 5px; margin: 15px 0; font-size: 0.9em;">ℹ️ Label dataset asli: <strong>${food.original_label}</strong> → Model memprediksi: <strong>${food.label}</strong></div>` : ''}
                <button class="btn-analyze" onclick="analyzeFood(${food.id})">🔍 Bandingkan dengan Model Lain</button>
                <div id="analysisResult" class="result-box"></div>
            `;

            document.getElementById('foodModal').style.display = 'block';
        }

        function getModelName(model) {
            const names = {'random_forest': 'Random Forest', 'naive_bayes': 'Naive Bayes', 'kmeans': 'K-Means Clustering', 'svm': 'SVM'};
            return names[model] || model;
        }

        function closeModal() {
            document.getElementById('foodModal').style.display = 'none';
        }

        async function analyzeFood(foodId) {
            const food = foodsData.find(f => f.id == foodId);
            if (!food) return;

            const resultDiv = document.getElementById('analysisResult');
            resultDiv.innerHTML = '<div class="loading">Menganalisis...</div>';
            resultDiv.classList.add('show');

            const formData = new FormData();
            formData.append('calories', food.calories);
            formData.append('proteins', food.proteins);
            formData.append('fat', food.fat);
            formData.append('carbohydrate', food.carbohydrate);
            formData.append('model', selectedModel);

            try {
                const response = await fetch('predict.php', {method: 'POST', body: formData});
                const result = await response.json();
                
                resultDiv.className = 'result-box show ' + getLabelClass(result.label_name || food.label);
                resultDiv.innerHTML = `<h3>${result.title}</h3><p>${result.description}</p><div style="margin-top: 15px;"><strong>Confidence:</strong> ${result.confidence}%</div>`;
            } catch (error) {
                resultDiv.className = 'result-box show label-sangat-buruk';
                resultDiv.innerHTML = '<h3>Error</h3><p>Gagal menganalisis makanan. Silakan coba lagi.</p>';
            }
        }

        window.onclick = function(event) {
            if (event.target === document.getElementById('foodModal')) closeModal();
        }
    </script>
</body>
</html>
