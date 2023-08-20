# Chessmanager analysis

Application for downloading and analysing data from chess tournaments from chessmanager.com

---

1. Download data from chessmanager.com to JSON file

    ```
    cd backend
    python download.py
    ```

2. Run backend server
    ```
    cd backend
    ./run_prod.sh
    ```

3. Run frontend website (development mode)
    ```
    npm run dev
    ```

4. Run frontend website (production mode):
    ```
    npm run build
    ```