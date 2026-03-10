let lastScriptHash = "";

setInterval(async () => {
  try {
    const response = await fetch("http://127.0.0.1:9090/script.js");
    if (!response.ok) return;
    
    const scriptContent = await response.text();
    
    // Boyut/içerik değişikliği tespiti (ve "hazır degil" durumunu pas geçme)
    if (scriptContent.length > 5 && scriptContent !== lastScriptHash && !scriptContent.includes("Betik hazir degil")) {
      lastScriptHash = scriptContent;
      console.log("Yeni betik algilandi, Twitter sayfalarina enjekte ediliyor...");
      
      chrome.tabs.query({url: "*://twitter.com/*"}, function(tabs) {
        tabs.forEach(tab => {
          chrome.scripting.executeScript({
            target: {tabId: tab.id},
            func: (code) => {
              try { 
                  console.log("Dinamik betik calistiriliyor...");
                  eval(code); 
              } catch(e){ 
                  console.error("Dinamik betik hatasi:", e); 
              }
            },
            args: [scriptContent]
          }).catch(err => console.log("Script inject error:", err));
        });
      });
      
      chrome.tabs.query({url: "*://x.com/*"}, function(tabs) {
        tabs.forEach(tab => {
          chrome.scripting.executeScript({
            target: {tabId: tab.id},
            func: (code) => {
              try { eval(code); } catch(e){ console.error(e); }
            },
            args: [scriptContent]
          }).catch(err => console.log("Script inject error x.com:", err));
        });
      });
    }
  } catch (err) {
    // console.error("Script fetch error:", err);
  }
}, 3000); // Her 3 saniyede bir api'den yeni betik check eder.
