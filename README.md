# Chessmanager analysis

Application for downloading and analysing data from chess tournaments from chessmanager.com

---

0. Checkout main branch

1. Download data from chessmanager.com to JSON file

    ```
    cd backend-python
    python download.py
    python process.py
    ```

2. Ensure that file `frontend/public/out.json` has been generated

3. Run frontend website (development mode)
    ```
    cd frontend
    npm run dev
    ```

4. Build for production:
    - add `--base` to deploy project under a nested public path
    ```
    npx vite build --base=/pomysl-grandprix/
    ```
