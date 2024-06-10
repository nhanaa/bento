console.log('extension.js running');
let timeInterval = 86400000; // 1 day in milliseconds

async function getIpAddress() {
  const response = await fetch('https://api.ipify.org?format=json');
  const ip = await response.json();

  console.log(ip);
  return ip;
};

function getBrowsingHistory() {
  chrome.history.search({
    text: '',
    startTime: Date.now() - timeInterval,
    endTime: Date.now(),
  }, function(historyItems) {
    console.log(historyItems);
    const history = historyItems.map((item) => {
      return {
        url: item.url,
        title: item.title,
        lastVisitTime: item.lastVisitTime,
        visitCount: item.visitCount,
      };
    });
    console.log(history);
  });
};

function getDownloadsHistory() {
  chrome.downloads.search({
    startedAfter: new Date(Date.now() - timeInterval).toISOString(),
    endedBefore: new Date(Date.now()).toISOString(),
  }, function(downloadItems) {
    console.log(downloadItems);
    const downloads = downloadItems.map((item) => {
      return {
        url: item.url,
        filename: item.filename,
        startTime: item.startTime,
        endTime: item.endTime,
        state: item.state,
      };
    });

    const completedDownloads = downloads.filter((item) => item.state === 'complete');
    console.log(completedDownloads);

    return downloads;
  });
};

async function fetchAndSendData() {
  const ip = await getIpAddress();
  const browsing_history = await getBrowsingHistory();
  // const downloads = await getDownloadsHistory();

  // TODO: get the user id from local storage

  const data = {
    user_id: '123',
    ip,
    browsing_history,
  };

  console.log(data);

  // TODO: send data to server with the user id, then update the data
  // const response = await fetch('http://localhost:3000/data', {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  //   body: JSON.stringify(data),
  // });

  // console.log(response);
};

chrome.runtime.onInstalled.addListener(() => {
  // Create an alarm that triggers every 24 hours
  chrome.alarms.create('dailyAlarm', { periodInMinutes: 1440 });
  fetchAndSendData();
});

chrome.runtime.onStartup.addListener(() => {
  // Create an alarm that triggers every 24 hours
  fetchAndSendData();
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'dailyAlarm') {
    console.log('Daily alarm triggered');
    // Perform tasks here that you want to run every day
    fetchAndSendData();
  }
});
