//
//  SelectSeatsView.swift
//  MovieTicketing
//
//  Created by izundu ngwu on 4/23/22.
//

import SwiftUI

struct SelectSeatsView: View {
    var id: String
    @EnvironmentObject var firestoreManager: FirestoreManager
    @State private var movie = Movie()
    @State private var reserved = [Int]()
    @State private var reservedSeats = Set<Int>()
    @State private var newReservedSeats = Set<Int>()
    @State private var isShowingPayView = false
    var body: some View {
        VStack{
            Spacer(minLength: 50)
            Text("Seating View").font(.title3)
            Spacer(minLength: 50)
            VStack{
                Text("SCREEN").font(.largeTitle)
                    .padding(.vertical, 70.0)
                    .padding(.horizontal, 100.0)
                    .overlay {
                        RoundedRectangle(cornerRadius: 3)
                            .stroke(lineWidth: 1)
                            .foregroundColor(.black)
                
                    }
                Spacer(minLength: 40)
                ForEach(0..<10) { row in
                    HStack{
                        ForEach(0..<8){ col in
                            Button{
                                let seat = row*8+col
                                 if (!reservedSeats.contains(seat)){
                                     if(newReservedSeats.contains(seat)){
                                         newReservedSeats.remove(seat)
                                     }
                                     else {
                                         newReservedSeats.insert(seat)
                                     }
                                 }
                                
                            } label: {
                                Text("R\(row+1) C\(col+1)").font(.caption2)
                            }
                            .frame(width: 40, height: 20)
                            .foregroundColor(.black)
                            .background(seatColor(seat: row*8+col))
                            .clipShape(RoundedRectangle(cornerRadius: 3))
                            .overlay {
                                RoundedRectangle(cornerRadius: 3)
                                    .stroke(lineWidth: 0.5)
                                    .foregroundColor(.black)
                            }
                        }
                    }
                }
            }
            Spacer(minLength: 40)
            NavigationLink(isActive: $isShowingPayView) {
                ReserveAndPayView(seats: newReservedSeats, movie: self.movie)
            } label: {
                EmptyView()
            }
            Button {
                reserveAndPay()
            } label: {
                Text("Reserve/Pay")
                    .padding()
                    .background(.blue)
                    .foregroundColor(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 8))
            }
            Spacer(minLength: 100)
        }.onAppear {
            getSeating(fromMovie: id)
        }.navigationTitle(Text(movie.title))
    }
    func getSeating(fromMovie: String){
        movie = Movie()
    }
    func seatColor(seat: Int) -> Color {
        if(reservedSeats.contains(seat)){
            return Color.red
        }
        else{
            if(newReservedSeats.contains(seat)){
                return Color.green
            }
            else {return Color.white}
        }
    }
    func reserveAndPay(){
        reserved = firestoreManager.getReserveSeats(forDocument: id)
        for(
        isShowingPayView = true
        
    }
}

struct SelectSeatsView_Previews: PreviewProvider {
    static var previews: some View {
        SelectSeatsView(id: "")
    }
}
