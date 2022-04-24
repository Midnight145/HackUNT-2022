//
//  User.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import Foundation

struct User: Identifiable, Hashable {
    var id: ObjectIdentifier
    var name: String
    var age : Int
}
