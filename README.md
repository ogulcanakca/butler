# MCP Servers Usage in Agents

This project utilizes FastAgent to interact with various services through Model Context Protocol (MCP) servers. MCP servers provide a standardized protocol that enables AI agents to communicate with external systems, offering access to various functionalities such as capturing screenshots, querying weather information, sending emails, interacting with Slack workspaces, and managing SQLite databases. This integration allows users to experience a rich and interactive environment with comprehensive service connectivity while maintaining best practices for agent-based system architecture.

## Running the Project

To get this project up and running, follow these steps after navigating to the root directory of the project:

1.  **Initialize the virtual environment with `uv`:**
    ```bash
    uv init
    ```
2.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
3.  **Add `ruff` for linting (optional but recommended):**
    ```bash
    uv add ruff
    ```
4.  **Check the code with `ruff` (optional):**
    ```bash
    uv run ruff check
    ```
5.  **Lock dependencies:**
    ```bash
    uv lock
    ```
6.  **Sync dependencies (install them based on the lock file):**
    ```bash
    uv sync
    ```
7.  **Run the agent:**
    ```bash
    uv run agent.py
    ```

## FastAgent

FastAgent is the primary client used in this project to orchestrate and manage interactions with the different MCP servers. It allows for seamless communication and data exchange between the agent and the services.

## Configured MCP Servers

Below is a list of MCP servers configured for this project. For detailed implementation and setup instructions, please refer to their respective repositories.

### Filesystem MCP Server

*   **Description**: Provides functionalities to interact with the local filesystem.
*   **Implementation Details**: [MCP server filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
*   **Configuration in `fastagent.config.yaml`**:
    ```yaml
    filesystem:
        command: "npx"
        args: ["-y", "@modelcontextprotocol/server-filesystem", "."]
    ```

### Google Maps MCP Server

*   **Description**: Enables interaction with Google Maps services. 
*   **Implementation Details**: [MCP server google-maps](https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps)
*   **Configuration in `fastagent.config.yaml`**:
    ```yaml
    google-maps:
        command: "npx"
        args: ["-y", "@modelcontextprotocol/server-google-maps"]
        env:
            GOOGLE_MAPS_API_KEY: "AIza----------------------------------------------------"
    ```
    **Obtaining a Google Maps API Key**: Please refer to [documentation](https://developers.google.com/maps/documentation/javascript/get-api-key) for instructions on obtaining a Google Maps API key.
    
    **Note**: For full functionality, make sure to enable almost all Maps APIs (Places API (New), Directions API, Geocoding API, etc.) for your GCP project.
### Slack MCP Server

*   **Description**: Allows the agent to communicate and interact with Slack.
*   **Implementation Details**: [MCP server slack](https://github.com/modelcontextprotocol/servers/tree/main/src/slack)
*   **Configuration in `fastagent.config.yaml`**:
    ```yaml
    slack:
        command: "npx"
        args: [
            "-y",
            "@modelcontextprotocol/server-slack"
        ]
        env:
            SLACK_BOT_TOKEN: "xoxb----------------------------------------------------"
            SLACK_TEAM_ID: "T-----------"
            SLACK_CHANNEL_IDS: "C------------, C------------, C------------"
    ```

### SQLite MCP Server

*   **Description**: Provides an interface to interact with an SQLite database.
*   **Implementation Details**: [MCP server sqlite](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite)
*   **Configuration in `fastagent.config.yaml`**:
    ```yaml
    sqlite:
        command: "uv"
        args: [
            "--directory",
            "./src/sqlite",
            "run",
            "mcp-server-sqlite",
            "--db-path",
            "test.db"
        ]
    ```
* **Note**: The test.db file is located in the ./src/sqlite/ directory.

### Screenshot Capture MCP Server

*   **Description**: Provides functionalities to capture screenshots of the user's screen.
*   **Implementation Details**: This server is implemented as a local Python script. Refer to `./created_mcp_servers/screenshot_capture.py` for details.
*   **Configuration in `fastagent.config.yaml`**:
    ```yaml
    screenshot_capture:
        command: "python"
        args: ["./created_mcp_servers/screenshot_capture.py"]
    ```

### Weather API MCP Server

*   **Description**: Provides weather information for any city.
*   **Implementation Details**: This server is implemented as a local Python script. Refer to `./created_mcp_servers/weather_api.py` for details.
*   **Configuration in `fastagent.config.yaml`**:
    ```yaml
    weather_api:
        command: "python"
        args: ["./created_mcp_servers/weather_api.py"]
    ```
    **Note**: This server interacts with an external weather API. Ensure any necessary API keys or configurations required by `./created_mcp_servers/weather_api.py` are correctly set up in your environment or the script.

### Serper Search MCP Server

*   **Description**: Enables the agent to perform internet searches using the Serper API and retrieve results.
*   **Implementation Details**: This server is implemented as a local Python script. Refer to `./created_mcp_servers/serper_search.py` for details.
*   **Configuration in `fastagent.config.yaml`**:
    ```yaml
    serper_search:
        command: "python"
        args: ["./created_mcp_servers/serper_search.py"]
    ```
    **Note**: This server interacts with the Serper API. Ensure any necessary API keys or configurations required by `./created_mcp_servers/serper_search.py` are correctly set up in your environment or the script.

### Gmail MCP Server

*   **Description**: Allows the agent to interact with Gmail for sending and receiving emails.
*   **Implementation Details**: Utilizes the `@gongrzhe/server-gmail-autoauth-mcp` package. More information can be found at [MCP server gmail-autoauth](https://github.com/gongrz/server-gmail-autoauth-mcp).
*   **Configuration in `fastagent.config.yaml`**:
    ```yaml
    gmail:
        command: "npx"
        args: ["@gongrzhe/server-gmail-autoauth-mcp"]
    ```
    **Note**: This server uses `@gongrzhe/server-gmail-autoauth-mcp` which is designed to simplify Gmail authentication. However, initial setup or user consent might be required. Refer to the server's documentation for specific authentication procedures and requirements.

## Agents

This project defines several agents, each with a specific role, orchestrated by FastAgent:

*   **`route`**: This agent acts as a router, directing incoming requests to the appropriate specialized agent based on the nature of the request. It utilizes the following agents: `chat_agent`, `screenshot_agent`, `weather_agent`, `search_agent`, `gmail_agent`, `maps_agent`, `slack_agent`, `sqlite_agent`, and `fallback_agent`.
*   **`orchestrate`**: This agent manages the overall flow and coordination between agents, starting with the `route` agent.
*   **`chat_agent`**: Handles direct conversations with the user in Turkish, responding to greetings and general chat.
*   **`screenshot_agent`**: Captures screenshots of the user's screen when requested.
*   **`weather_agent`**: Provides weather information for any city requested by the user.
*   **`search_agent`**: Performs internet searches based on user queries and presents the results.
*   **`gmail_agent`**: Manages Gmail interactions, such as sending and receiving emails.
*   **`maps_agent`**: Performs various map-related operations, including geocoding, reverse geocoding, place searches, getting place details, calculating distances, retrieving elevation data, and generating directions.
*   **`slack_agent`**: Interacts with Slack, enabling actions like listing channels, sending messages, replying to messages, reacting with emojis, fetching channel history, retrieving thread replies, listing users, and getting user profiles. All responses are in Turkish.
*   **`sqlite_agent`**: Interacts with an SQLite database, allowing it to execute SQL queries, list tables, fetch table schemas, and perform other database operations. Responses to the user are in Turkish.
*   **`fallback_agent`**: Handles requests that cannot be processed by any of the other specialized agents. It politely informs the user in Turkish that the request is outside its current capabilities and suggests alternative actions the user can take (e.g., chat, screenshot, weather, search, email, maps, Slack, or database operations).

## Usage Examples

Here are some example questions or commands you can use with the agents. These will typically be processed by the `orchestrate` and `route` agents to direct them to the appropriate specialized agent.

### `chat_agent`

*   "Merhaba, nasılsın?"
*   "Bana bir fıkra anlatır mısın?"

### `screenshot_agent`

*   "Ekranımın görüntüsünü alır mısın?"
*   "Bir ekran görüntüsü yakala."

### `weather_agent`

*   "İstanbul için hava durumu nedir?"
*   "Ankara'da şu an hava nasıl?"

### `search_agent`

*   "Türkiye'nin en yüksek dağı hangisidir?"
*   "Yapay zeka alanındaki son gelişmeler nelerdir?"

### `gmail_agent`

*   "Gelen kutumda yeni e-posta var mı?"
*   "`arkadas@example.com` adresine 'Selam' konulu bir e-posta gönder, içeriği 'Merhaba, nasılsın?' olsun."

### `maps_agent`

*   "Eyfel Kulesi'nin koordinatlarını verir misin?"
*   "Ankara Kalesi'nden Anıtkabir'e yol tarifi oluştur."
*   İzmir Saat Kulesi'nden Konak Pier'e arabayla gitmek ne kadar sürer?


### `slack_agent`

*   "`#genel` kanalına 'Herkese merhaba, günaydın!' mesajını yolla."
*   "Slack'teki aktif kullanıcıları listeler misin?"

### `sqlite_agent`

*   "`urunler` tablosundaki tüm verileri göster."
*   "Veritabanımda hangi tabloların olduğunu söyler misin?"
*   "test.db veritabanında 'notlar' adında yeni bir tablo oluştur. Bu tabloda 'id' (INTEGER PRIMARY KEY AUTOINCREMENT), 'baslik' (TEXT NOT NULL) ve 'icerik' (TEXT) adında üç sütun olsun."

### `fallback_agent`

*(This agent handles requests that other agents cannot. The following are examples of such requests that would trigger the `fallback_agent`.)*

*   "Bana bir resim çizer misin?"
*   "Yarın piyasalar nasıl olacak tahmin edebilir misin?"
