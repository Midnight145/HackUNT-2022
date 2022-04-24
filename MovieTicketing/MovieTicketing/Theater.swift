//
//  Theater.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import Foundation

struct Theater: Identifiable, Equatable {
    var id: ObjectIdentifier
    var number: String
    var capacity = 100
    var available = 100
    var reserved = 0
}
