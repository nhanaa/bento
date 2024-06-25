const userId = "tin";
const folderId = "ml";

async function docCreation() {
  try {
    let folderName = document.getElementById("folderName").value;
    let folderDesc = document.getElementById("folderDesc").value;
    let combined_str = folderName + " " + folderDesc; // Ensure you format the string as required by your API
    const url1 = `http://127.0.0.1:8000/get_links/${userId}/`;
    const url2 = `http://127.0.0.1:8000/process_documents/${userId}/${folderId}/`;

    const { data: responseData } = await axios.post(url1, {
      query: combined_str,
    });
    displayLinks(responseData);
    await axios.post(url2, {
      links_list: responseData["links_list"],
    });
    let element = document.getElementById("status");
    element.innerHTML = "done :)";
  } catch (error) {
    console.error("Error during document creation:", error);
    alert("Failed to create document: " + error.message);
  }
}
function displayLinks(response) {
  const listElement = document.getElementById("linksList");

  // Clear existing list items if any
  listElement.innerHTML = "";

  // Loop through each link in the response and create a list item
  response.links_list.forEach((link) => {
    const listItem = document.createElement("li");
    const linkElement = document.createElement("a");
    linkElement.href = link;
    linkElement.textContent = link;
    listItem.appendChild(linkElement);
    listElement.appendChild(listItem);
  });
}

async function sendChat() {
  try {
    url = `http://127.0.0.1:8000/chat/${userId}/${folderId}/`;
    let message = document.getElementById("chatQuestion").value;
    const { data: responseData } = await axios.post(url, {
      text: message,
    });
    const answerElement = document.getElementById("chatAnswer");
    answerElement.innerHTML = responseData["output"];
  } catch (error) {
    console.error("Error during document creation:", error);
    alert("Failed to create document: " + error.message);
  }
}
