//
//  Seats.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import Foundation

struct Seat: Identifiable, Equatable, Hashable {
    var id = UUID().uuidString
    var user =  UUID().uuidString
    var theater = UUID().uuidString
    var movie = UUID().uuidString
    var number = 1
    var reserved = false
}
