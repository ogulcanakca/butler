import asyncio
from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.request_params import RequestParams

fast = FastAgent("fast-agent-örneği")

@fast.router(
  name="route",                          
  agents=["chat_agent", "screenshot_agent", "weather_agent", "search_agent", "gmail_agent", "maps_agent", "slack_agent", "sqlite_agent", "fallback_agent"], 
  model="haiku",                  
  use_history=False,                     
  human_input=False
  )
async def route():
    pass

@fast.orchestrator(
  name="orchestrate",
  agents=["route"],
  model="haiku"
)
async def orchestrate():
    pass

@fast.agent(
    name="chat_agent",
    instruction="""
    Sen kullanıcılarla doğrudan Türkçe sohbet eden bir ajansın. 
    Selamlaşmalara ve günlük konuşmalara Türkçe yanıt verirsin.
    Kullanıcı mesajlarına doğrudan ve kişisel olarak cevap ver.
    Yönlendirme veya analiz yapmak yerine, sanki gerçek bir sohbette konuşuyormuş gibi cevap ver.
    
    Örnek:
    Kullanıcı: Merhaba
    Sen: Merhaba! Size nasıl yardımcı olabilirim?
    
    Kullanıcı: Nasılsın?
    Sen: İyiyim, teşekkür ederim! Siz nasılsınız?
    
    Her zaman Türkçe konuş ve yanıt ver. Asla İngilizce kullanma.
    """,
    model="haiku",
    use_history=True,
    request_params=RequestParams(temperature=0.7),
    human_input=True
)
async def chat_agent():
    pass

@fast.agent(
    name="screenshot_agent",
    instruction="Ekran görüntüsü yakalayan yardımcı bir ajansın. Kullanıcı istediğinde onun ekranının görüntüsünü yakalayabilirsin.",
    servers=["screenshot_capture"],
    model="haiku",
    use_history=True,
    request_params=RequestParams(temperature=0.7),
    human_input=True
)
async def screenshot_agent():
    pass

@fast.agent(
    name="weather_agent",
    instruction="Hava durumu bilgisi sağlayan yardımcı bir ajansın. Kullanıcı istediğinde herhangi bir şehrin hava durumunu gösterebilirsin.",
    servers=["weather_api"],
    model="haiku",
    use_history=True,
    request_params=RequestParams(temperature=0.7),
    human_input=True
)
async def weather_agent():
    pass

@fast.agent(
    name="search_agent",
    instruction="İnternet araması yapan yardımcı bir ajansın. Kullanıcı istediğinde web'de arama yapabilir ve sonuçları gösterebilirsin.",
    servers=["serper_search"],
    model="haiku",
    use_history=True,
    request_params=RequestParams(temperature=0.7),
    human_input=True
)
async def search_agent():
    pass

@fast.agent(
    name="gmail_agent",
    instruction="E-posta gönderme ve alma gibi görevleri yerine getiren bir ajansın. Kullanıcının Gmail hesaplarıyla etkileşim kurabilirsin.",
    servers=["gmail"],
    model="haiku",
    use_history=True,
    request_params=RequestParams(temperature=0.7),
    human_input=True
)
async def gmail_agent():
    pass

@fast.agent(
    name="maps_agent",
    instruction="Harita ile ilgili çeşitli işlemleri gerçekleştiren bir ajansın. Adresleri koordinatlara çevirebilir, koordinatları adreslere çevirebilir, yerleri arayabilir, yer detaylarını alabilir, mesafeleri hesaplayabilir, yükseklik bilgilerini alabilir ve yol tarifleri oluşturabilirsin.",
    servers=["google-maps"],
    model="haiku",
    use_history=True,
    request_params=RequestParams(temperature=0.7),
    human_input=True
)
async def maps_agent():
    pass

@fast.agent(
    name="slack_agent",
    instruction="""Slack ile ilgili çeşitli işlemleri gerçekleştiren bir ajansın. 
    Kanalları listeleyebilir, kanallara mesaj gönderebilir, mesajlara yanıt verebilir, mesajlara emoji ile tepki verebilir, kanal geçmişini alabilir, mesaj dizisi yanıtlarını alabilir, kullanıcıları listeleyebilir ve kullanıcı profillerini alabilirsin.
    Her zaman Türkçe yanıt ver.""",
    servers=["slack"],
    model="haiku",
    use_history=True,
    request_params=RequestParams(temperature=0.7),
    human_input=True
)
async def slack_agent():
    pass

@fast.agent(
    name="sqlite_agent",
    instruction="""Sen bir SQLite veritabanı ile etkileşim kurabilen yardımcı bir ajansın.
    SQL sorguları çalıştırabilir, veritabanındaki tabloları listeleyebilir, tablo şemalarını getirebilir ve veritabanı üzerinde çeşitli işlemler yapabilirsin.
    Kullanıcının veritabanı ile ilgili isteklerini Türkçe olarak yanıtla.
    Örnek:
    Kullanıcı: Kullanıcılar tablosundaki tüm kayıtları göster.
    Sen: Elbette, kullanıcılar tablosundaki tüm kayıtları getiriyorum. [SONUÇLAR]
    Kullanıcı: Hangi tablolar var?
    Sen: Veritabanında şu tablolar mevcut: [TABLO LİSTESİ]
    Her zaman Türkçe yanıt ver.""",
    servers=["sqlite"],
    model="haiku",
    use_history=True,
    request_params=RequestParams(temperature=0.7),
    human_input=True
)
async def sqlite_agent():
    pass

@fast.agent(
    name="fallback_agent",
    instruction="""
    Sen yalnızca diğer ajanların (chat, screenshot, weather, search, gmail, maps, slack ve sqlite) işleyemediği istekleri alırsın.
    
    Bu tür durumlarda, kullanıcıya kibarca Türkçe olarak cevap ver ve şunları açıkla:
    1. İsteğinin mevcut yeteneklerimizin dışında olduğunu
    2. Nasıl yardımcı olabileceğini - örn. sohbet, ekran görüntüsü alma, hava durumu bilgisi, web araması, e-posta işlemleri, harita işlemleri, Slack işlemleri veya veritabanı (SQLite) işlemleri
    
    İstekleri reddettiğinde her zaman nazik ol ve alternatif önerilerde bulun.
    Her zaman Türkçe yanıt ver.
    """,
    model="haiku",
    use_history=True,
    request_params=RequestParams(temperature=0.4),
    human_input=True
)
async def fallback_agent():
    pass

async def main():
    async with fast.run() as agent_app:
        await agent_app.interactive(agent="orchestrate")

if __name__ == "__main__":
    asyncio.run(main())