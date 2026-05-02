# نظام RAG باستخدام PostgreSQL و GitHub Models

هذا المشروع يهدف إلى بناء نظام RAG (Retrieval-Augmented Generation) قوي ومبسط.
الفكرة الأساسية هي استخدام قاعدة بيانات **PostgreSQL** مع إضافة `pgvectorscale` لتخزين النصوص وتحويلها إلى متجهات (Vectors) للبحث عنها بسرعة وكفاءة عالية، بالإضافة إلى الاعتماد على **GitHub Models** لمعالجة الذكاء الاصطناعي.

## فكرة العمل باختصار:
- بنأخذ النصوص ونحولها لأرقام (Embeddings) باستخدام `text-embedding-3-small` من خلال **GitHub Models**.
- بنخزن الأرقام دي في قاعدة بيانات **PostgreSQL**.
- لما المستخدم يسأل سؤال، بنحول السؤال لنفس الصيغة الرقمية ونبحث عن أقرب النصوص ليه في قاعدة البيانات عشان نجاوب عليه بدقة.

## المكونات الأساسية:
1. **GitHub Models**: لتحويل النصوص لـ Embeddings باستخدام الـ GitHub Token بتاعك.
2. **PostgreSQL**: قاعدة البيانات اللي بنخزن فيها الداتا.
3. **Pgvectorscale**: إضافة لـ PostgreSQL بتخلي عملية البحث عن النصوص المشابهة سريعة جداً.
4. **Docker**: لتشغيل بيئة قاعدة البيانات بسهولة وبدون تعقيد.

## خطوات التشغيل:
1. انسخ ملف `app/example.env` وسميه `app/.env`.
2. افتح ملف `app/.env` وحط فيه الـ **GitHub Personal Access Token (PAT)** بتاعك في المتغير `OPENAI_API_KEY`.
3. شغل قاعدة البيانات باستخدام Docker عن طريق الأمر: 
   ```bash
   docker compose up -d
   ```
4. نزل مكتبات بايثون المطلوبة:
   ```bash
   pip install -r requirements.txt
   ```
5. لتجهيز الداتا وإدخالها في قاعدة البيانات، شغل:
   ```bash
   python app/insert_vectors.py
   ```
6. للبحث وتجربة النظام، استخدم:
   ```bash
   python app/similarity_search.py
   ```
