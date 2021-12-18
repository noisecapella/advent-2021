use std::fs::File;
use std::io::prelude::*;

fn calc_score(contents: &str) -> i64 {
    let mut scores = Vec::new();
    for line in contents.split("\n") {
	let mut stack = Vec::new();
	let mut corrupt = false;
	if line.len() == 0 {
	    continue;
	}

	for c in line.chars() {
	    match c {
		'{' | '[' | '<' | '(' => { stack.push(c); }
		'}' => {
		    if stack.last() == Some(&'{') {
			stack.pop();
		    } else {
			corrupt = true;
			break;
		    }
		}
		']' => {
		    if stack.last() == Some(&'[') {
			stack.pop();
		    } else {
			corrupt = true;
			break;
		    }
		}
		'>' => {
		    if stack.last() == Some(&'<') {
			stack.pop();
		    } else {
			corrupt = true;
			break;
		    }
		}
		')' => {
		    if stack.last() == Some(&'(') {
			stack.pop();
		    } else {
			corrupt = true;
			break;
		    }
		}
		_ => {
		    panic!("invalid char {}", c);
		}
	    }
	}

	let mut score = 0;
	while stack.len() > 0 {
	    let c = stack.pop();
	    let points_for_char = match c {
		Some('[') => 2,
		Some('(') => 1,
		Some('{') => 3,
		Some('<') => 4,
		_ => panic!("unexpected character")
	    };
	    score *= 5;
	    score += points_for_char;
	}
	scores.push(score);
    }
    scores.sort();
    
    return scores[scores.len() / 2];
}

fn main() -> std::io::Result<()> {
    let mut file = File::open("input.txt")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let score = calc_score(&contents);
    println!("score: {}", score);
    Ok(())
}
