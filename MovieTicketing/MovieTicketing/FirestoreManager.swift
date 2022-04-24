//
//  FirestoreManager.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/24/22.
//

import Foundation
import Firebase
import FirebaseFirestore

class FirestoreManager: ObservableObject {
    let db = Firestore.firestore()
    let movies = Firestore.firestore().collection("Movies")
    var movieTitles = [String]()
    var movie = Movie()
    var movieTimes = [String]()
    var movieDateReff = Firestore.firestore().collection("Movies")
    var movieTimeReff = Firestore.firestore().collection("Movies").document(" ")
    var allseats = [Int]()
    func createMovie(_ movie: Movie){
        let movieDate = movie.showdate.formatted(date: .long, time: .omitted)
        let movieTime = movie.showdate.formatted(date: .omitted, time: .shortened)
        let newMovieTitleRef = movies.document("\(movie.title)")
        let newMovieDateRef = newMovieTitleRef.collection(movieDate)
        let newMovieTimeRef = newMovieDateRef.document(movieTime)
        newMovieTitleRef.setData([
            "agerating": "\(movie.agerating)"
        ]) { err in
            if let err = err {
                print("Error writing document: \(err)")
            } else {
                print("Document successfully written!")
            }
        }
//        newMovieTitleRef.setData([
//            "\(movieDate)" : [
//                "theater": movie.theater + 1,
//                "seats" : movie.seats,
//                "time" : Timestamp(date: movie.showdate)
//            ]
//        ])
        newMovieTimeRef.setData([
                "theater": movie.theater + 1,
                "seats" : movie.seats
        ]){ err in
            if let err = err {
                print("Error writing document: \(err)")
            } else {
                print("Document successfully written!")
            }
        }
    }
    func getMovies() -> [String]{
        movies.getDocuments() { (querySnapshot, err) in
            if let err = err {
                print("Error getting documents: \(err)")
            } else {
                self.movieTitles = [String]()
                for document in querySnapshot!.documents {
                    self.movieTitles.append(document.documentID)
                }
            }
        }
        return movieTitles
    }
    func getMovieTimes(fromTitle title: String, dateString: String) -> [String]{
        let movieRef = movies.document(title)
        self.movie.title = title
        movieRef.getDocument{ (document, error) in
            if let document = document, document.exists {
//                let age = document.value(forKey: "agerating") as! String
//                self.movie.agerating = Int(age) ?? 18
            } else {
                print("Document does not exist")
            }
        }
        let movieDate = movieRef.collection(dateString)
        movieDateReff = movieDate
        movieDate.getDocuments() { (querySnapshot, err) in
            if let err = err {
                print("Error getting documents: \(err)")
            } else {
                self.movieTimes = [String]()
                for document in querySnapshot!.documents {
                    self.movieTimes.append(document.documentID)
                }
            }
        }
        return movieTimes
    }
    func getReserveSeats(forDocument: String) -> [Int]{
        movieDateReff.document("\(forDocument)").getDocument{(document, error) in
            if let document = document, document.exists {
//                let age = document.value(forKey: "agerating") as! String
//                self.movie.agerating = Int(age) ?? 18
                if let alseats = document.get("seats") as? [Int] {
                    self.allseats = alseats
                    return alseats
                }
            } else {
                print("Document does not exist")
            }
        }
    }
    func reserveSeats(forDocument: String, seats: Set<Int>){
        movieDateReff.document("\(forDocument)").getDocument{(document, error) in
            if let document = document, document.exists {
//                let age = document.value(forKey: "agerating") as! String
//                self.movie.agerating = Int(age) ?? 18
                if let alseats = document.get("seats") as? [Int] {
                    self.allseats = alseats
                }
            } else {
                print("Document does not exist")
            }
        }
        let seatss = seats.map{$0}
        for index in seatss {
            self.movie.seats[index] = 1
        }
        
    }
//    titanic.getDocument { (document, error) in
//        if let document = document, document.exists {
//            self.movie.title  = title
//
//            let dataDescription = document.data().map(String.init(describing:)) ?? "nil"
//            print("Document data: \(dataDescription)")
//        } else {
//            print("Document does not exist")
//        }
//    }
}
