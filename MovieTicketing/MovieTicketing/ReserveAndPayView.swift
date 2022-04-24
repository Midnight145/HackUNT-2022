//
//  ReserveAndPayView.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/24/22.
//

import SwiftUI

struct ReserveAndPayView: View {
    @State var seats = Set<Int>()
    private var seatsArr: Array<Int>{
        return seats.map{$0}
    }
    @State var movie = Movie()
    var body: some View {
        VStack(spacing: 20){
            Spacer()
            Text("The following seats were reserved:")
            List{
                ForEach(seatsArr, id: \.self) { seat in
                    Text("Row \(calculateRowAndCol(seat).0), Col \(calculateRowAndCol(seat).1)")
                }
            }.listStyle(.plain)
            Text("for")
            Text("\(movie.title)").font(.title2)
            Spacer()
        }.navigationTitle("Seats Reserved!")
            .navigationBarTitleDisplayMode(.automatic)
    }
    func calculateRowAndCol(_ seat: Int) -> (Int, Int) {
        let col = seat % 8
        let row = seat / 8
        return (row + 1, col + 1)
    }
}

struct ReserveAndPayView_Previews: PreviewProvider {
    static var previews: some View {
        ReserveAndPayView()
    }
}
