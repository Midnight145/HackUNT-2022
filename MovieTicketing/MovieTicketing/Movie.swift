//
//  Movie.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import Foundation

struct Movie: Identifiable, Equatable, Hashable {
    var id = UUID().uuidString
    var title = "*insert movie name here*"
    var agerating = 18
    var showtime: String {
        let time = showdate.formatted(date: .omitted, time: .shortened)
        return time
    }
    var showdate = Date.now
    var theater = 1
    var seats = Array(repeating: 0, count: 80)
}

class MovieObject: ObservableObject {
    var movie = Movie()
}
