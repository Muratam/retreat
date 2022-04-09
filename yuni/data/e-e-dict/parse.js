'use strict';
// https://stackoverflow.com/questions/41768215/english-json-dictionary-with-word-word-type-and-definition
function load_e_e_dict() {
  const fs = require('fs');
  let files = fs.readdirSync(".");
  let result = {}
  for (let file of files) {
    if (!file.endsWith(".json")) continue;
    let rawdata = fs.readFileSync(file);
    let data = JSON.parse(rawdata);
    for (let k in data) {
      result[k] = data[k];
      let array_meanings = [];
      let mapped_meanings = result[k]["MEANINGS"];
      for (let i = 1; ; i++) {
        let meanings = mapped_meanings[`${i}`];
        if (!meanings) break;
        // if (meanings[3]) console.log(meanings[3]);
        array_meanings.push(meanings)
      }
      result[k]["MEANINGS"] = array_meanings;
    }
  }
  return result;
}
let dict = load_e_e_dict();
// <Word> -> { ANTONYMS: ["", ...], SYNONYMS: ["", ...], MEANINGS: [
// "Noun", <MEANING>, [CONTEXT], [EXAMPLES]]}
// console.log(dict["AVIATION"]);
// console.log(dict["AVIATION"]["MEANINGS"]);

// まずは単純にMEANINGの関係から
let meaning_map = {};
const meaning_typeset = ['Noun', 'Verb', 'Adverb', 'Adjective'];
for (let k in dict) {
  let words = new Set();
  for (let meaning of dict[k]["MEANINGS"]) {
    // console.log([k, meaning[0], meaning[1]])
    for (let word of meaning[1].replace(/([^a-zA-Z0-9]+)/g, " $1 ").split(" ")) {
      if (word.match(/%s+/) || word === "") continue;
      words.add(word.toLowerCase());
    }
  }
  if (words.size === 0) continue;
  meaning_map[k.toLowerCase()] = words;
}
let rev_meaning_map = {};
for (let k in meaning_map) {
  for (let word of meaning_map[k]) {
    if (!rev_meaning_map[word]) {
      rev_meaning_map[word] = new Set();
    }
    rev_meaning_map[word].add(k)
  }
}
console.log([...meaning_map["dog"]]);
console.log(Object.keys(meaning_map).length)
console.log([...rev_meaning_map["dog"]]);
console.log(Object.keys(rev_meaning_map).length)
console.log(meaning_map["task"]);
let rev_meaning_array = [];
for (let k in rev_meaning_map) {
  rev_meaning_array.push([k, rev_meaning_map[k].size]);
}
rev_meaning_array.sort((x, y) => y[1] - x[1]);
console.log(rev_meaning_array);
